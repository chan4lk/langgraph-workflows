from dataclasses import dataclass
from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain.schema import BaseOutputParser
from langchain.prompts import PromptTemplate
from typing import Optional
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

@dataclass
class DesignState:
    topic: str
    user_comments: Optional[str] = None
    summary: Optional[str] = None
    dfd: Optional[str] = None
    db_schema: Optional[str] = None

def prompt_llm(prompt_file, topic, user_comments):
    with open(os.path.join(os.path.dirname(__file__), prompt_file), 'r') as f:
        prompt = PromptTemplate.from_template(f.read())
    chain = prompt | llm
    return chain.invoke({"topic": topic, "user_comments": user_comments})

def generate_summary(state: DesignState):
    topic = state.topic
    print(topic)
    if not topic:
        raise ValueError("Missing 'topic' in state")
    summary = prompt_llm("prompts/design_summary.txt", topic, state.user_comments)
    return {"summary": summary, "topic": topic}  # 🧠 Pass 'topic' forward


def generate_dfd(state: DesignState):
    dfd = prompt_llm("prompts/generate_dfd.txt", state.summary, state.user_comments)
    return {"dfd": dfd}

def generate_db_schema(state: DesignState):
    schema = prompt_llm("prompts/generate_db_schema.txt", state.summary, state.user_comments)
    return {"db_schema": schema}

def build_graph():
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    graph = StateGraph(DesignState)
    graph.add_node("generate_summary", generate_summary)
    graph.add_node("generate_dfd", generate_dfd)
    graph.add_node("generate_db_schema", generate_db_schema)

    graph.set_entry_point("generate_summary")
    graph.add_edge("generate_summary", "generate_dfd")
    graph.add_edge("generate_dfd", "generate_db_schema")
    graph.add_edge("generate_db_schema", END)

    return graph.compile(checkpointer=memory)

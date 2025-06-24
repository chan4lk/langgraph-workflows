import os
from langchain_memgraph.graphs.memgraph import Memgraph
from langchain_memgraph.chains.graph_qa import MemgraphQAChain
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List

from langchain_memgraph.graphs.memgraph import Memgraph
from langchain_memgraph.chains.graph_qa import MemgraphQAChain
from langchain_openai import ChatOpenAI

class MyMemgraphClient(Memgraph):
    def get_schema(self):
        # Example: Return node labels and relationship types
        node_labels = self.execute_and_fetch("MATCH (n) RETURN DISTINCT labels(n)")
        rel_types = self.execute_and_fetch("MATCH ()-[r]->() RETURN DISTINCT type(r)")
        return {"node_labels": node_labels, "rel_types": rel_types}

graph = MyMemgraphClient(
    url="bolt://localhost:7687",
    username="",
    password=""
)
schema_str = graph.get_schema()  # Call the method to get the schema string
qa_chain = MemgraphQAChain.from_llm(
    ChatOpenAI(temperature=0),
    graph=graph,
    graph_schema=schema_str,  # Now this is a string
)
# Define agent state for LangGraph
class State(TypedDict):
    messages: List

# Node: Use QA chain to answer questions from the knowledge graph
def agent_node(state: State):
    user_message = state['messages'][-1].content
    response = qa_chain.invoke(user_message)
    return {'messages': state['messages'] + [AIMessage(content=response['result'])]}

# Build LangGraph workflow
graph_builder = StateGraph(State)
graph_builder.add_node("agent", agent_node)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)
workflow = graph_builder.compile()

# Simulate a conversation
initial_state = {'messages': [HumanMessage(content="Tell me about Zelda.")]}
result = workflow.invoke(initial_state)
for msg in result['messages']:
    print(f"{msg.type}: {msg.content}")
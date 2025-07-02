from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage
from typing import Sequence
from dataclasses import dataclass, field
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langmem import create_memory_store_manager
from pydantic import BaseModel
from langchain_core.runnables import RunnableConfig

from zep_cloud.client import AsyncZep
from zep_cloud import Message
import os
import asyncio

zep = AsyncZep(api_key=os.environ.get('ZEP_API_KEY'))

def _format_prompt(context: str, knowledge_base_content: str, question: str) -> str:
    """
    Formats a prompt string for the LLM, ensuring consistency across different nodes.
    """
    return f"""You are a helpful AI assistant. Use the provided "Knowledge Base" to answer the "Question".
If the "Knowledge Base" does not contain enough information, state that you cannot answer based on the provided information.

Previous conversation context:
{context}

Knowledge Base:
{knowledge_base_content}

Question: {question}"""

rules = [
    "Every order is assigned a unique order number.",
    "Customers can check their order status by providing the order number.",
    "If the order is shipped, provide the tracking number and estimated delivery date.",
    "If the order is processing, inform the customer and provide an estimated shipping date.",
    "If the order is delayed, apologize and provide the reason and new estimated delivery date.",
    "If the order is delivered, confirm delivery and ask for feedback.",
    "If the order number is invalid, ask the customer to double-check or provide more information.",
    "Always address the customer politely and thank them for their order."
]

summary = (
    "Customers can inquire about their order status using their order number. "
    "Depending on the order’s state (processing, shipped, delayed, or delivered), provide relevant details such as tracking information, estimated dates, or delivery confirmation. "
    "Always respond politely, thank the customer, and request clarification if the order number is invalid."
)

# Set up LangMem store and agent
store = InMemoryStore(
    index={
        "dims": 1536,
        "embed": "openai:text-embedding-3-small",
    }
)

config = {"configurable": {"langgraph_user_id": "user123"}}
class RuleTriple(BaseModel):
    subject: str
    predicate: str
    object: str
    context: str | None = None

manager = create_memory_store_manager(
    "openai:gpt-4o-mini",
    schemas=[RuleTriple],
    instructions="Extract all rules about customer order handling as triples.",
    enable_inserts=True,
    enable_deletes=True,
    store=store,
)

rules_as_messages = [{"role": "user", "content": rule} for rule in rules]

manager.invoke({"messages": rules_as_messages}, config=config)

# Agent state
@dataclass
class State:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)
    rules_response: AnyMessage | None = None
    summary_response: AnyMessage | None = None
    langmem_response: AnyMessage | None = None
    zep_response: AnyMessage | None = None
    current_rules: list[str] = field(default_factory=list)
    current_summary: str = ""

# LLM for rules and summary nodes
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

async def _invoke_llm(state: State, knowledge_base_content: str) -> AnyMessage:
    question = state.messages[-1].content
    context = state.messages[-2].content
    prompt = _format_prompt(
        context=context,
        knowledge_base_content=knowledge_base_content,
        question=question
    )
    return await llm.ainvoke([HumanMessage(content=prompt)])

# Node: Full rules
async def rules_node(state: State):
    return { "rules_response": await _invoke_llm(state, "\n".join(state.current_rules or rules)) }

# Node: Summary
async def summary_node(state: State):
    return { "summary_response": await _invoke_llm(state, state.current_summary or summary) }

# Node: LangMem agent
async def langmem_node(state: State):
    memories = manager.search(
        query=state.messages[-1].content,
        config=config,
    )
    memory_context = "\n".join([m.value.subject + " " + m.value.predicate + " " + m.value.object for m in memories if hasattr(m, 'value')])
    return { "langmem_response": await _invoke_llm(state, memory_context) }

# Node: Zep Agent
async def zep_node(state: State):
    memories = await search_facts(zep_user_id, state.messages[-1].content, 10)
    memory_context = "\n".join(memories)
    return { "zep_response": await _invoke_llm(state, memory_context) }

# Build the workflow
workflow = StateGraph(State)
workflow.add_node("rules", rules_node)
workflow.add_node("summary", summary_node)
workflow.add_node("langmem", langmem_node)
workflow.add_node("zep", zep_node)  

workflow.add_edge(START, "rules")
workflow.add_edge("rules", "summary")
workflow.add_edge("summary", "langmem")
workflow.add_edge("langmem", "zep")
workflow.add_edge("zep", END)

graph = workflow.compile()

zep_user_id = "zep_9d5d9e29f1422101f16b0d88747a50fea605009046867164a34b4189e6ec8bed"

async def search_facts(user_name: str, query: str, limit: int = 5) -> list[str]:
    """Search for facts in all conversations had with a user.
    
    Args:
        user_name (str): The user's name.
        query (str): The search query.
        limit (int): The number of results to return. Defaults to 5.

    Returns:
        list: A list of facts that match the search query.
    """
    results = await zep.graph.search(
        user_id=user_name, query=query, limit=limit
    )
    edges = results.edges
    return [edge.fact for edge in edges]


async def search_nodes(user_name: str, query: str, limit: int = 5) -> list[str]:
    """Search for nodes in all conversations had with a user.
    
    Args:
        user_name (str): The user's name.
        query (str): The search query.
        limit (int): The number of results to return. Defaults to 5.

    Returns:
        list: A list of node summaries for nodes that match the search query.
    """
    nodes = await zep.graph.search(
        user_id=user_name, query=query, limit=limit
    )
    return [node.summary for node in nodes.edges]

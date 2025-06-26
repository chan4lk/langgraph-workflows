# Import core components (1)
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage
from typing import Sequence
from dataclasses import dataclass, field
from langgraph.graph import add_messages
from typing_extensions import Annotated

# Define agent state for LangGraph
@dataclass
class State:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )

# Set up storage (2)
store = InMemoryStore(
    index={
        "dims": 1536,
        "embed": "openai:text-embedding-3-small",
    }
) 

# Create an agent with memory capabilities (3)
agent = create_react_agent(
    "openai:gpt-4o-mini",
    prompt="You are a helpful AI assistant. Answer questions based on the provided context and tools. If you don't know the answer, say 'I don't know'.",
    tools=[
        # Memory tools use LangGraph's BaseStore for persistence (4)
        create_manage_memory_tool(namespace=("memories",)),
        create_search_memory_tool(namespace=("memories",)),
    ],
    store=store,
)

workflow = StateGraph(State)
workflow.add_node("agent", agent)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)
graph = workflow.compile()



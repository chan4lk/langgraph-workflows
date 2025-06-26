# Import core components (1)
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage
from typing import Sequence
from dataclasses import dataclass, field
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI
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

@tool
def get_memory(config: RunnableConfig):
    """Get a memory from the store"""
    return store.get("memories", namespace=(config.user_id,))

@tool
def add_memory(state: State, config: RunnableConfig):
    """Add the last user message to the store as a memory with summary"""
    memory = state.messages[-1].content
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    last_summary = get_memory(config)
    prompt = f"""
    You are a helpful AI assistant whos summary the last user message with last summary. 
    
    Last summary: {last_summary}
    Last user message: {memory}
    """
    summary = llm.invoke(prompt=prompt)
    store.add("memories", namespace=(config.user_id,), value=summary)

# Create an agent with memory capabilities (3)
agent = create_react_agent(
    "openai:gpt-4o-mini",
    prompt="You are a helpful AI assistant. Answer questions based on the provided context and tools. If you don't know the answer, say 'I don't know'.",
    tools=[
        # Memory tools use LangGraph's BaseStore for persistence (4)
        get_memory,
        add_memory,
        ],
    store=store,
)

workflow = StateGraph(State)
workflow.add_node("agent", agent)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)
graph = workflow.compile()



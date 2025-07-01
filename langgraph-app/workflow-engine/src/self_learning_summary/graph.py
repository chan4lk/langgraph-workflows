from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from typing import Sequence
from dataclasses import dataclass, field
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langmem import create_memory_manager, create_search_memory_tool
from pydantic import BaseModel
from langchain_core.runnables import RunnableConfig

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


class RuleTriple(BaseModel):
    subject: str
    predicate: str
    object: str
    context: str | None = None

manager = create_memory_manager(
    "openai:gpt-4o-mini",
    schemas=[RuleTriple],
    instructions="Extract all rules about customer order handling as triples.",
    enable_inserts=True,
    enable_deletes=True,
)

rules_text = "\n".join(rules)
memories = manager.invoke({"messages": [{"role": "system", "content": rules_text}]})
triples = [m.content for m in memories if hasattr(m, "content")]

# Agent state
@dataclass
class State:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)
    rules_response: AnyMessage | None = None
    summary_response: AnyMessage | None = None
    langmem_response: AnyMessage | None = None

# Set up LangMem store and agent
store = InMemoryStore(
    index={
        "dims": 1536,
        "embed": "openai:text-embedding-3-small",
    }
)

langmem_agent = create_react_agent(
    "openai:gpt-4o-mini",
    prompt="You are a helpful AI assistant. Answer questions based on the provided context and tools. If you don't know the answer, say 'I don't know'.",
    tools=[
        manager.as_tool(RuleTriple),
    ],
    store=store,
)

search_tool = create_search_memory_tool(store=store, namespace="self_learning_summary")

# LLM for rules and summary nodes
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Node: Full rules
def rules_node(state: State):
    question = state.messages[-1].content
    context= state.messages[-2].content
    prompt = (
        "Rules:\n" + "\n".join(rules) +
        f"\n\n{context}\n\nQuestion: {question}"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return { "rules_response": response }

# Node: Summary
def summary_node(state: State):
    question = state.messages[-1].content
    context= state.messages[-2].content
    prompt = (
        "Summary:\n" + summary +
        f"\n\n{context}\n\nQuestion: {question}"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return { "summary_response": response }

# Node: LangMem agent
def langmem_node(state: State, config: RunnableConfig):
    # Get the latest message and context
    question = state.messages[-1].content
    context = state.messages[-2].content
    
    # Retrieve relevant memories
    memories = search_tool.invoke(
        input={"query": question},
        config=config,
    )
    memory_context = "\n".join([m.content for m in memories if hasattr(m, 'content')])
    
    # Prepare the full context with memories
    full_context = f"""Previous conversation context:
{context}

Relevant rules and knowledge:
{memory_context}

Question: {question}"""
    
    # Invoke the agent with the full context and conversation history
    response = langmem_agent.invoke({
        "messages": [
            *[
                {"role": "user" if i % 2 == 0 else "assistant", "content": msg.content}
                for i, msg in enumerate(state.messages[:-1])  # All messages except the last one
            ],
            {"role": "user", "content": full_context}
        ]
    })
    
    # Save the current interaction to memory
    manager.invoke({
        "messages": [
            {"role": "system", "content": "Remember this interaction for future reference."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": response.content if hasattr(response, 'content') else str(response)}
        ]
    })
    
    return {"langmem_response": response}

# Build the workflow
workflow = StateGraph(State)
workflow.add_node("rules", rules_node)
workflow.add_node("summary", summary_node)
workflow.add_node("langmem", langmem_node)

workflow.add_edge(START, "rules")
workflow.add_edge("rules", "summary")
workflow.add_edge("summary", "langmem")
workflow.add_edge("langmem", END)

graph = workflow.compile()

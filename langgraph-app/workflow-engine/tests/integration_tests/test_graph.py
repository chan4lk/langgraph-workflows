import pytest
from langsmith import unit

from react_agent.graph import graph
from self_learning.graph import graph as self_learning_graph
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.asyncio
@unit
async def test_react_agent_simple_passthrough() -> None:
    res = await graph.ainvoke(
        {"messages": [("user", "Who is the founder of LangChain?")]},
        {"configurable": {"system_prompt": "You are a helpful AI assistant."}},
    )

    assert "harrison" in str(res["messages"][-1].content).lower()


@pytest.mark.asyncio
@unit
async def test_self_learning_agent_simple_passthrough() -> None:
    res = await self_learning_graph.ainvoke(
        {"messages": [("user", "What is the capital of France?")]},
    )

    assert "paris" in str(res["messages"][-1].content).lower()

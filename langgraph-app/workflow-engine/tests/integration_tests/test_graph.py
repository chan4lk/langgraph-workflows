import pytest
from langsmith import unit

from react_agent.graph import graph
from self_learning.graph import graph as self_learning_graph
from self_learning_graphiti.graph import get_initialized_graph 
from self_learning_summary.graph import graph as self_learning_summary_graph 
import dotenv

dotenv.load_dotenv()


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

@pytest.mark.asyncio
@unit
async def test_self_learning_graphiti_agent_simple_passthrough() -> None:
    # Get an initialized graph instance
    print("Initializing Graphiti...")
    graph, node_uuid = await get_initialized_graph('chandima')
    assert graph is not None, "Failed to initialize graph"
    print("Graphiti initialized successfully")
        
    # Run the test with the initialized graph
    res = await graph.ainvoke(
        {"messages": [("user", "What is the status of my order?")], "user_node_uuid": node_uuid, "user_name": "chandima"},
    )
        
    # Get the last message content in lowercase for case-insensitive check
    last_message = str(res["messages"][-1].content).lower()
    print(f"Agent response: {last_message}")
        
    # Check if the response contains 'order' (case-insensitive)
    assert "order" in last_message, f"Expected 'order' in response, got: {last_message}"
        

@pytest.mark.asyncio
@unit
async def test_self_learning_summary_agent_simple_passthrough() -> None:
    res = await self_learning_summary_graph.ainvoke(
        {"messages": [("user", "I have the order 1245 is pending status"),("user", "What is the status of my order?")]},
        {"configurable": {"user_id": "chandima"}}
    )

    assert "order" in str(res["messages"][-1].content).lower()


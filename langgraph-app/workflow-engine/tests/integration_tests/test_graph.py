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
        {"messages": [
            ("user", "Assume order 134 is shipped, tracking number 123456, estimated delivery July 1"),
            ("user", "What is the status of my order 134?")
        ]},
        {"configurable": {"user_id": "chandima"}}
    )

    assert "123456" in str(res['summary_response'].content).lower()
    assert "123456" in str(res['langmem_response']["messages"][-1].content).lower()
    assert "123456" in str(res['rules_response'].content).lower()


@pytest.mark.asyncio
@unit
async def test_self_learning_summary_with_custom_rules() -> None:
    custom_rules = [
        "Order status inquiries require an order number.",
        "For shipped orders, provide tracking and estimated delivery.",
        "For delayed orders, provide reason and new estimated delivery."
    ]
    custom_summary = "Customers can inquire about order status; provide details based on order state."

    res = await self_learning_summary_graph.ainvoke(
        {
            "messages": [
                ("user", "Assume order 789 is delayed due to weather, new estimated delivery August 10"),
                ("user", "What is the status of my order 789?")
            ]
        },
        {
            "configurable": {
                "user_id": "test_user_custom_rules",
                "current_rules": custom_rules,
                "current_summary": custom_summary
            }
        }
    )

    # Verify that the responses contain expected information based on the custom rules/summary
    assert "delayed" in str(res['rules_response'].content).lower()
    assert "august 10" in str(res['rules_response'].content).lower()
    
    assert "order status" in str(res['summary_response'].content).lower()
    assert "details based on order state" in str(res['summary_response'].content).lower()

    # LangMem and Zep responses should also reflect the context, but their content might vary more
    # We'll check for general relevance rather than specific phrases from custom_rules/summary
    assert "delayed" in str(res['langmem_response'].content).lower() or "august 10" in str(res['langmem_response'].content).lower()
    assert "delayed" in str(res['zep_response'].content).lower() or "august 10" in str(res['zep_response'].content).lower()

"""
Node utilities for the credit approval workflow.
This module provides common functionality for workflow nodes to reduce duplication.
"""

from typing import List, Union,Callable
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command

from credit_agents_deterministic.state import CreditState
from credit_agents_deterministic.messages import (
    FilterableHumanMessage, 
    normalize_messages, 
    create_messages, 
    reverse_messages, 
    filter_messages
)

def get_messages(state: CreditState, result: dict, tool_name: str) -> dict:
    """Process agent result and update message state
    
    Args:
        state: Current workflow state
        result: Result from agent invocation
        tool_name: Name of the tool/agent that generated the result
        
    Returns:
        Dictionary with all_messages and chat_messages
    """
    # Create a new message from the agent result
    new_message = FilterableHumanMessage(
        content=result["messages"][-1].content, 
        name=tool_name,
        # Set show_in_chat based on whether this tool should be filtered
        show_in_chat=tool_name not in state.filter_tools
    )
    
    # Add the new message to all existing messages
    all_messages = state.all_messages + [new_message]
    
    # Get messages that should be shown in chat (show_in_chat=True)
    chat_messages = filter_messages(all_messages, show_in_chat=True)
    
    return { 
        "all_messages": all_messages, 
        "chat_messages": chat_messages 
    }

def prepare_messages_for_agent(state: CreditState) -> List[Union[HumanMessage, AIMessage]]:
    """
    Prepare messages for agent invocation by normalizing and converting as needed.
    
    Args:
        state: Current workflow state
        
    Returns:
        List of messages ready for agent invocation
    """
    # Normalize state.messages to ensure proper message objects
    if state.messages:
        state.messages = normalize_messages(state.messages)
    
    # Initialize all_messages if needed
    if not state.all_messages or len(state.all_messages) == 0:
        state.all_messages = create_messages(state.messages, True)
    
    # Get messages for the LLM (either from state.messages or by converting all_messages back)
    return state.messages if len(state.all_messages) == 0 else reverse_messages(state.all_messages)

def create_node_handler(
    agent: Callable, 
    tool_name: str, 
    next_node: str = "supervisor"
) -> Callable[[CreditState], Command]:
    """
    Create a standard node handler for the workflow.
    
    Args:
        agent: Agent to invoke
        tool_name: Name of the tool/agent
        next_node: Name of the next node to go to
        
    Returns:
        Node handler function
    """
    def node_handler(state: CreditState) -> Command:
        # Prepare messages for the agent
        messages_for_llm = prepare_messages_for_agent(state)
        
        # Invoke the agent
        result = agent.invoke({"messages": messages_for_llm})
        
        # Process the result
        messages = get_messages(state, result, tool_name)
        
        # Return command to update state and go to next node
        return Command(
            update={
                "messages": messages["chat_messages"],
                "all_messages": messages["all_messages"]
            },
            goto=next_node,
        )
    
    return node_handler

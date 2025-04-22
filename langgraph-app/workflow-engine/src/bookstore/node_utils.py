"""
Node utilities for the bookstore workflow.
This module provides utility functions for handling node interactions.
"""

from typing import Dict, List, Any, Optional, Callable, Literal, cast
from langgraph.types import Command
from langchain_core.messages import BaseMessage

from .types import BookstoreState
from .messages import normalize_messages, create_messages, reverse_messages

def prepare_messages_for_agent(state: BookstoreState) -> List[Dict[str, Any]]:
    """
    Prepare messages for an agent from the current state.
    
    Args:
        state: Current workflow state
        
    Returns:
        Messages formatted for agent consumption
    """
    # Normalize state.messages to ensure proper message objects
    if state.messages:
        state.messages = normalize_messages(state.messages)
    
    # Initialize all_messages if needed
    if not state.all_messages or len(state.all_messages) == 0:
        state.all_messages = create_messages(state.messages, True)
    
    # Return messages in format agents expect
    return reverse_messages(state.all_messages)

def get_messages(
    state: BookstoreState, 
    result: Dict[str, Any],
    agent_name: str
) -> Dict[str, Any]:
    """
    Process the result from an agent and update messages.
    
    Args:
        state: Current workflow state
        result: Result from agent
        agent_name: Name of the agent
        
    Returns:
        Updated messages
    """
    # Get the agent's messages from the result
    agent_messages = result.get("messages", [])
    
    # Process messages for chat display and all_messages
    chat_messages = []
    all_messages = state.all_messages.copy() if state.all_messages else []
    
    for message in agent_messages:
        # Add to all_messages regardless of display settings
        all_messages.append(message)
        
        # Only add to chat_messages if show_in_chat is True
        if not hasattr(message, "show_in_chat") or message.show_in_chat:
            chat_messages.append(message)
    
    return {
        "chat_messages": chat_messages,
        "all_messages": all_messages
    }

def create_node_handler(
    agent: Callable,
    agent_name: str,
    next_node: str
) -> Callable[[BookstoreState], Command[Literal[str]]]:
    """
    Create a standard node handler function for an agent.
    
    Args:
        agent: Agent function to invoke
        agent_name: Name of the agent
        next_node: Name of the next node to go to
        
    Returns:
        Node handler function
    """
    def node_handler(state: BookstoreState) -> Command[Literal[str]]:
        # Prepare messages for the agent
        messages_for_llm = prepare_messages_for_agent(state)
        
        # Invoke the agent
        result = agent.invoke({"messages": messages_for_llm})
        
        # Process the result
        messages_result = get_messages(state, result, agent_name)
        
        # Return command to update state and go to next node
        return Command(
            update={
                "messages": messages_result["chat_messages"],
                "all_messages": messages_result["all_messages"]
            },
            goto=next_node,
        )
    
    return node_handler

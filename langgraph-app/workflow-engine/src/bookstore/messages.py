"""
Message handling utilities for the bookstore workflow.
This module provides functionality for normalizing and managing messages between agents.
"""

from typing import Dict, List, Any, Optional, Union, cast
from dataclasses import dataclass
from langchain_core.messages import (
    HumanMessage, 
    AIMessage, 
    SystemMessage,
    BaseMessage
)

@dataclass
class FilterableHumanMessage(HumanMessage):
    """Human message that can be filtered based on agent type."""
    name: Optional[str] = None
    show_in_chat: bool = True

def normalize_messages(messages: List[Union[Dict[str, Any], BaseMessage]]) -> List[BaseMessage]:
    """
    Normalize messages to ensure they are all BaseMessage objects.
    
    Args:
        messages: List of messages (dicts or BaseMessage objects)
        
    Returns:
        List of normalized BaseMessage objects
    """
    normalized = []
    
    for message in messages:
        if isinstance(message, BaseMessage):
            normalized.append(message)
        elif isinstance(message, dict):
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "human":
                normalized.append(
                    FilterableHumanMessage(
                        content=content,
                        name=message.get("name"),
                        show_in_chat=message.get("show_in_chat", True)
                    )
                )
            elif role == "ai":
                normalized.append(AIMessage(content=content))
            elif role == "system":
                normalized.append(SystemMessage(content=content))
        
    return normalized

def create_messages(
    messages: List[Union[Dict[str, Any], BaseMessage]], 
    include_history: bool = True
) -> List[BaseMessage]:
    """
    Create normalized messages from input messages.
    
    Args:
        messages: Input messages
        include_history: Whether to include message history
        
    Returns:
        List of normalized messages
    """
    # Normalize messages first
    normalized = normalize_messages(messages)
    
    if include_history:
        return normalized
    else:
        # Only return the last message
        return [normalized[-1]] if normalized else []

def reverse_messages(messages: List[BaseMessage]) -> List[Dict[str, Any]]:
    """
    Convert BaseMessage objects to dictionaries.
    
    Args:
        messages: List of BaseMessage objects
        
    Returns:
        List of message dictionaries
    """
    result = []
    
    for message in messages:
        if isinstance(message, SystemMessage):
            result.append({"role": "system", "content": message.content})
        elif isinstance(message, HumanMessage):
            if isinstance(message, FilterableHumanMessage):
                result.append({
                    "role": "human", 
                    "content": message.content,
                    "name": message.name,
                    "show_in_chat": message.show_in_chat
                })
            else:
                result.append({"role": "human", "content": message.content})
        elif isinstance(message, AIMessage):
            result.append({"role": "ai", "content": message.content})
    
    return result

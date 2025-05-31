"""
Message handling utilities for the meta prompter Windsurf workflow.
"""
from typing import List, Dict, Any, Union, Sequence
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage, BaseMessage


def normalize_messages(messages: Union[List[Dict[str, Any]], Sequence[BaseMessage]]) -> List[BaseMessage]:
    """
    Normalize different message formats into a standard BaseMessage list.
    
    Args:
        messages: Messages in various formats (dict or BaseMessage objects)
        
    Returns:
        List[BaseMessage]: Normalized list of BaseMessage objects
    """
    normalized_messages = []
    
    if not messages:
        return []
    
    for message in messages:
        if isinstance(message, BaseMessage):
            # Already a BaseMessage, just add it
            normalized_messages.append(message)
        elif isinstance(message, dict):
            # Convert dict to appropriate message type
            if message.get("type") == "human" or message.get("role") == "user":
                normalized_messages.append(HumanMessage(content=message.get("content", "")))
            elif message.get("type") == "ai" or message.get("role") == "assistant":
                normalized_messages.append(AIMessage(content=message.get("content", "")))
            # Add more message types as needed
        else:
            # Skip invalid message formats
            continue
    
    return normalized_messages


def format_messages_for_llm(messages: Sequence[BaseMessage]) -> List[Dict[str, Any]]:
    """
    Format messages for LLM consumption.
    
    Args:
        messages: List of BaseMessage objects
        
    Returns:
        List[Dict]: Messages formatted for LLM
    """
    formatted_messages = []
    
    for message in messages:
        if isinstance(message, HumanMessage):
            formatted_messages.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            formatted_messages.append({"role": "assistant", "content": message.content})
        # Add more message types as needed
    
    return formatted_messages


def extract_last_message_content(messages: Sequence[BaseMessage]) -> str:
    """
    Extract the content from the last message in the sequence.
    
    Args:
        messages: List of BaseMessage objects
        
    Returns:
        str: Content of the last message, or empty string if no messages
    """
    if not messages:
        return ""
    
    return messages[-1].content if hasattr(messages[-1], "content") else ""

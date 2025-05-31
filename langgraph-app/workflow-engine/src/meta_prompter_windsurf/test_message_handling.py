"""
Test script for the message handling utilities in the meta prompter Windsurf workflow.
"""
from typing import Dict, List, Any
from langchain_core.messages import HumanMessage, AIMessage

from meta_prompter_windsurf.utils import (
    normalize_messages,
    format_messages_for_llm,
    extract_last_message_content
)


def test_normalize_messages():
    """Test the normalize_messages function with different message formats."""
    # Test with dictionary messages
    dict_messages = [
        {"type": "human", "content": "Hello, I need an app"},
        {"role": "assistant", "content": "I can help with that"}
    ]
    
    normalized = normalize_messages(dict_messages)
    print("Normalized dictionary messages:")
    for msg in normalized:
        print(f"  - Type: {type(msg).__name__}, Content: {msg.content}")
    
    # Test with BaseMessage objects
    base_messages = [
        HumanMessage(content="I want to build a task manager"),
        AIMessage(content="Great, I can help you design that")
    ]
    
    normalized = normalize_messages(base_messages)
    print("\nNormalized BaseMessage objects:")
    for msg in normalized:
        print(f"  - Type: {type(msg).__name__}, Content: {msg.content}")
    
    # Test with mixed message types
    mixed_messages = [
        {"type": "human", "content": "What tech stack should I use?"},
        AIMessage(content="It depends on your requirements")
    ]
    
    normalized = normalize_messages(mixed_messages)
    print("\nNormalized mixed message types:")
    for msg in normalized:
        print(f"  - Type: {type(msg).__name__}, Content: {msg.content}")
    
    return normalized


def test_format_messages_for_llm():
    """Test the format_messages_for_llm function."""
    messages = [
        HumanMessage(content="I need a web app for recipe sharing"),
        AIMessage(content="I'll help you build that"),
        HumanMessage(content="Can we use React?")
    ]
    
    formatted = format_messages_for_llm(messages)
    print("\nFormatted messages for LLM:")
    for msg in formatted:
        print(f"  - Role: {msg['role']}, Content: {msg['content']}")
    
    return formatted


def test_extract_last_message_content():
    """Test the extract_last_message_content function."""
    messages = [
        HumanMessage(content="First message"),
        AIMessage(content="Second message"),
        HumanMessage(content="Last message")
    ]
    
    content = extract_last_message_content(messages)
    print(f"\nExtracted last message content: {content}")
    
    # Test with empty messages
    empty_content = extract_last_message_content([])
    print(f"Extracted content from empty messages: '{empty_content}'")
    
    return content


if __name__ == "__main__":
    print("Testing message handling utilities...")
    test_normalize_messages()
    test_format_messages_for_llm()
    test_extract_last_message_content()
    print("\nAll tests completed!")

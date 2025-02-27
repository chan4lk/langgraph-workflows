"""Utility functions for the Slack lead processing workflow."""

from typing import Any, Dict, Optional
from typing_extensions import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage


def load_chat_model(model_name: str) -> BaseChatModel:
    """Load a chat model based on the model name.
    
    Args:
        model_name: The name of the model to load
        
    Returns:
        A chat language model
    """
    # In a real implementation, this would load the appropriate model
    # For demo purposes, we'll use a mock model
    provider, model = model_name.split("/", maxsplit=1) if "/" in model_name else ("openai", model_name)
    return init_chat_model(model, model_provider=provider)


def extract_slack_message(slack_event: Dict[str, Any]) -> str:
    """Extract the message content from a Slack event.
    
    Args:
        slack_event: The Slack event data
        
    Returns:
        The message content
    """
    # In a real implementation, this would extract the message from the Slack event
    # For demo purposes, we'll return a mock message
    slack_message = slack_event.get('slack_message', {})
    content = slack_message.get('content', '')
    if not content:
        return f"New lead from {slack_event.get('user', {}).get('name', 'Unknown')} in channel {slack_message.get('channel', 'Unknown')}"
    return content


def create_initial_message(slack_event: Dict[str, Any]) -> HumanMessage:
    """Create an initial message for the agent based on the Slack event.
    
    Args:
        slack_event: The Slack event data
        
    Returns:
        A human message with the Slack event information
    """
    message_content = f"""
A new lead has been posted on Slack:

User: {slack_event.get('user', {}).get('name', 'Unknown')}
Email: {slack_event.get('user', {}).get('email', 'Unknown')}
Channel: {slack_event.get('slack_message', {}).get('channel', 'Unknown')}
Timestamp: {slack_event.get('timestamp', 'Unknown')}

Please process this lead according to our workflow.
"""
    return HumanMessage(content=message_content)

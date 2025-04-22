"""
Utility functions for the bookstore workflow.
"""

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional

def load_chat_model(model_name: str = "openai/gpt-4o-mini") -> BaseChatModel:
    """
    Load a chat model based on the model name.
    
    Args:
        model_name: Name/path of the model to load
        
    Returns:
        Loaded chat model
    """
    # Currently only supports OpenAI models
    if "openai" in model_name:
        model_id = model_name.split("/")[-1]
        return ChatOpenAI(model=model_id, temperature=0.2)
    else:
        # Default fallback
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# langgraph-app/workflow-engine/src/swot_analyzer/utils.py
# Utility functions for SWOT analyzer

from typing import Any, Dict, Optional
from typing_extensions import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

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
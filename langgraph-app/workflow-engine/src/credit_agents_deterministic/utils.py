from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

def load_chat_model(model_name: str, temperature: float = 0.0) -> BaseChatModel:
    """Load a chat model based on the model name.
    
    Args:
        model_name: The name of the model to load, in format 'provider/model' or just 'model'
        temperature: The temperature to use for generation (0.0 to 1.0)
        
    Returns:
        A chat language model instance
    """
    try:
        # Parse provider and model name
        if "/" in model_name:
            provider, model = model_name.split("/", maxsplit=1)
        else:
            provider, model = "openai", model_name
        
        # Initialize the appropriate model based on provider
        if provider.lower() == "openai":
            return ChatOpenAI(
                model_name=model,
                temperature=temperature,
                streaming=False  # Disable streaming for tool use
            )
        else:
            # Default to OpenAI if provider not recognized
            print(f"Provider '{provider}' not recognized, defaulting to OpenAI")
            return ChatOpenAI(model_name="gpt-4o-mini", temperature=temperature)
    except Exception as e:
        print(f"Error loading chat model: {e}")
        # Return a fallback model
        return ChatOpenAI(model_name="gpt-4o-mini", temperature=temperature)
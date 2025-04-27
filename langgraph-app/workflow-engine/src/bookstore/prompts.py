"""
Prompts and agent creation utilities for the bookstore workflow.
This module centralizes all prompts and agent creation logic.
"""

from typing import List, Dict, Any, Callable
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel

# System prompts for different agents
SUPERVISOR_PROMPT_TEMPLATE = """
You are a supervisor tasked with managing a conversation between the
following workers: {members}. 
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
When the workflow is complete, respond with FINISH.
for providing book information use the book_info_provider agent.
for updating or adding books to the catalog use the catalog_updater agent
"""

AGENT_PROMPTS = {
    "book_info_provider": """
You run a popular and reputed bookstore. You are very knowledgeable about books in general 
and you can suggest books by genre / age.

When responding to queries:
1. First understand what the customer is asking about
2. Provide relevant information about books matching their query
3. Be detailed but concise in your responses
4. If they're asking about a specific book, provide details like author, genre, and a brief summary
5. If they're asking for recommendations, suggest 2-3 books that match their criteria

you cannot add books to the catalog on user request
""",
    
    "catalog_updater": """
You manage the catalog in a book store. The catalog has book title, author, genre, and age limit. 
You will add books to the catalog on user request, with all the necessary details.

When adding a book to the catalog:
1. Make sure you have all required information (title, author, genre, age limit)
2. If any information is missing, ask for it or make a reasonable assumption
3. When the update is complete, provide a confirmation message
4. Be thorough and accurate when recording book details
"""
}

def get_supervisor_prompt(members: List[str]) -> str:
    """
    Generate the supervisor prompt with the list of members.
    
    Args:
        members: List of worker names
        
    Returns:
        Formatted supervisor prompt
    """
    return SUPERVISOR_PROMPT_TEMPLATE.format(members=members)

def create_agent(
    agent_type: str, 
    llm: BaseChatModel, 
    tools: List[BaseTool] = None
) -> Callable:
    """
    Create an agent with the specified type, LLM, and tools.
    
    Args:
        agent_type: Type of agent to create (must be a key in AGENT_PROMPTS)
        llm: Language model to use
        tools: List of tools for the agent (optional)
        
    Returns:
        Created agent
    """
    if agent_type not in AGENT_PROMPTS:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    prompt = AGENT_PROMPTS[agent_type]
    
    # If no tools provided, use an empty list
    if tools is None:
        tools = []
        
    return create_react_agent(llm, tools=tools, prompt=prompt)

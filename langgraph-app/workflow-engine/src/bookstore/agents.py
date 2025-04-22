from typing import Dict, Any, Literal
from typing_extensions import TypedDict
from langgraph.types import Command
from bookstore.types import BookstoreState, NextStep
from bookstore.prompts import create_agent, get_supervisor_prompt
from bookstore.tools import search_catalog_tool, add_book_tool, get_book_tool
from bookstore.utils import load_chat_model
from bookstore.node_utils import prepare_messages_for_agent, get_messages
from bookstore.messages import normalize_messages, reverse_messages, create_messages

# Define workflow members (agent types)
MEMBERS = ["book_info_provider", "catalog_updater"]

# Options for the supervisor (all members plus FINISH)
OPTIONS = MEMBERS + ["FINISH"]

# Get the supervisor prompt
SYSTEM_PROMPT = get_supervisor_prompt(MEMBERS)

# Load the language model
LLM = load_chat_model("openai/gpt-4o-mini")

# Create the agents with their respective tools
AGENTS = {
    "book_info_provider": create_agent(
        "book_info_provider", 
        LLM, 
        [search_catalog_tool, get_book_tool]
    ),
    "catalog_updater": create_agent(
        "catalog_updater", 
        LLM, 
        [add_book_tool]
    )
}

# Supervisor Agent (Router)
def supervisor(state: BookstoreState) -> Command[Literal[*MEMBERS, "__end__"]]:
    """
    Supervisor agent that routes the workflow based on the user request.
    
    Args:
        state: Current workflow state
        
    Returns:
        Command with the next node to go to
    """
    # Normalize state.messages to ensure proper message objects
    if state.messages:
        state.messages = normalize_messages(state.messages)
        
    # Create base messages with system prompt
    base_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Initialize all_messages if needed
    if not state.all_messages or len(state.all_messages) == 0:
        state.all_messages = create_messages(state.messages, True)

    # Combine base messages with converted messages
    messages = base_messages + reverse_messages(state.all_messages)
    
    # Define the Router TypedDict for structured output
    class Router(TypedDict):
        next: Literal[*OPTIONS]
    
    # Get routing decision from LLM
    response = LLM.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    
    # If FINISH, go to end
    if goto == "FINISH":
        return Command(goto="__end__")
    
    # Otherwise, go to the specified node
    return Command(goto=goto)

# Create book_info_provider handler
def book_info_provider(state: BookstoreState) -> Command[Literal["supervisor"]]:
    """
    Book Info Provider agent that retrieves book information.
    
    Args:
        state: Current workflow state
        
    Returns:
        Command with updated state and next node
    """
    # Prepare messages for the agent
    messages_for_llm = prepare_messages_for_agent(state)
    
    # Invoke the agent
    result = AGENTS["book_info_provider"].invoke({"messages": messages_for_llm})
    
    # Process the result
    messages_result = get_messages(state, result, "book_info_provider")
    
    # Return command to update state and go to next node
    return Command(
        update={
            "messages": messages_result["chat_messages"],
            "all_messages": messages_result["all_messages"]
        },
        goto="supervisor",
    )

# Create catalog_updater handler
def catalog_updater(state: BookstoreState) -> Command[Literal["supervisor"]]:
    """
    Catalog Updater agent that adds books to the catalog.
    
    Args:
        state: Current workflow state
        
    Returns:
        Command with updated state and next node
    """
    # Prepare messages for the agent
    messages_for_llm = prepare_messages_for_agent(state)
    
    # Invoke the agent
    result = AGENTS["catalog_updater"].invoke({"messages": messages_for_llm})
    
    # Process the result
    messages_result = get_messages(state, result, "catalog_updater")
    
    # Return command to update state and go to next node
    return Command(
        update={
            "messages": messages_result["chat_messages"],
            "all_messages": messages_result["all_messages"]
        },
        goto="supervisor",
    )

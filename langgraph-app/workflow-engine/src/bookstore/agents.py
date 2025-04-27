from typing import Dict, Any, Literal
from typing_extensions import TypedDict
from langgraph.types import Command
from bookstore.types import BookstoreState 
from bookstore.prompts import create_agent, get_supervisor_prompt
from bookstore.tools import search_catalog_tool, add_book_tool, get_book_tool
from bookstore.utils import load_chat_model


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

    # Define the Router TypedDict for structured output
class Router(TypedDict):
    next: Literal[*OPTIONS]

# Supervisor Agent (Router)
def supervisor(state: BookstoreState) -> Command[Literal[*MEMBERS, "__end__"]]:
    """
    Supervisor agent that routes the workflow based on the user request.
    
    Args:
        state: Current workflow state
        
    Returns:
        Command with the next node to go to
    """
    
    # Create base messages with system prompt
    base_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    messages = base_messages + state.messages

    
    # Get routing decision from LLM
    response = LLM.with_structured_output(Router).invoke(messages)
    goto = response["next"]

    print(goto)
    
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
    messages_for_llm = state.messages
    
    # Invoke the agent
    result = AGENTS["book_info_provider"].invoke({"messages": messages_for_llm})
    
    # Process the result
    messages_result = result["messages"][-1]
    
    # Return command to update state and go to next node
    return Command(
        update={
            "messages": state.messages + [messages_result]
        },
        goto="supervisor",
    )

# Create catalog_updater handler
def catalog_updater(state: BookstoreState) -> Command[Literal["supervisor", "await_user"]]:
    """
    Catalog Updater agent that adds books to the catalog.
    Pauses for user input if more info is needed.
    """
    messages_for_llm = state.messages
    result = AGENTS["catalog_updater"].invoke({"messages": messages_for_llm})
    messages_result = result["messages"][-1]

    # Heuristic: if the message is a prompt for user info, pause for input
    content = getattr(messages_result, 'content', str(messages_result))
    needs_user = any(
        phrase in content.lower() for phrase in [
            "could you please provide", "would you like me to proceed", "please provide", "do you have any specific details"
        ]
    )
    if needs_user:
        print("needs user")
        return Command(
            update={"messages": state.messages + [messages_result]},
            goto="await_user",
        )
    return Command(
        update={"messages": state.messages + [messages_result]},
        goto="supervisor",
    )
   

"""
Main workflow graph for the credit approval system.
This module defines the workflow nodes and graph structure.
"""
from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from credit_agents_deterministic.utils import load_chat_model
from credit_agents_deterministic.state import CreditState
from credit_agents_deterministic.tools import (
    check_credit_score, 
    manual_approval, 
    perform_background_check, 
    validate_kyc, 
    make_final_decision
)
from credit_agents_deterministic.prompts import get_supervisor_prompt, create_agent
from credit_agents_deterministic.node_utils import (
    prepare_messages_for_agent, 
    get_messages, 
    create_node_handler
)
from credit_agents_deterministic.messages import (
    FilterableHumanMessage, 
    reverse_messages, 
    create_messages,
    normalize_messages
)

# Define workflow members (agent types)
MEMBERS = [
    "credit_score_checker", 
    "background_checker", 
    "final_decision", 
    "validate_kyc", 
    "manual_approver"
]

# Options for the supervisor (all members plus FINISH)
OPTIONS = MEMBERS + ["FINISH"]

# Get the supervisor prompt
SYSTEM_PROMPT = get_supervisor_prompt(MEMBERS)

# Load the language model
LLM = load_chat_model("openai/gpt-4o-mini")

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*OPTIONS]


# Create all agents
AGENTS = {
    "credit_score_checker": create_agent("credit_score_checker", LLM, [check_credit_score]),
    "background_checker": create_agent("background_checker", LLM, [perform_background_check]),
    "validate_kyc": create_agent("validate_kyc", LLM, [validate_kyc]),
    "manual_approver": create_agent("manual_approver", LLM, [manual_approval]),
    "final_decision": create_agent("final_decision", LLM, [make_final_decision])
}

def supervisor_node(state: CreditState) -> Command[Literal[*MEMBERS, "__end__"]]:
    """
    Supervisor node that decides which agent to call next.
    
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
    
    # Get routing decision from LLM
    response = LLM.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    
    # If FINISH, go to end
    if goto == "FINISH":
        return Command(goto="__end__")
    
    # Otherwise, go to the specified node
    return Command(goto=goto)

# Create standard node handlers for most agents
credit_score_node = create_node_handler(
    AGENTS["credit_score_checker"], 
    "credit_score_checker", 
    "supervisor"
)

background_checker_node = create_node_handler(
    AGENTS["background_checker"], 
    "background_checker", 
    "manual_approver"
)

validate_kyc_node = create_node_handler(
    AGENTS["validate_kyc"], 
    "validate_kyc", 
    "manual_approver"
)

final_decision_node = create_node_handler(
    AGENTS["final_decision"], 
    "final_decision", 
    "supervisor"
)

def manual_approver_node(state: CreditState) -> Command[Literal["supervisor"]]:
    """
    Manual approver node that requires user intervention.
    This is a custom node that can't use the standard handler.
    
    Args:
        state: Current workflow state
        
    Returns:
        Command with updated state and next node
    """
    # Prepare messages for the agent
    messages_for_llm = prepare_messages_for_agent(state)
    
    # Interrupt the user for manual approval
    approved = interrupt("Approve the application now?")
    label = "Approved" if approved else "Rejected"
    
    # Create approval message
    approval_message = FilterableHumanMessage(
        content=f"The application is '{label}'", 
        name="final_decision", 
        show_in_chat=False if "manual_approver" in state.filter_tools else True
    )
    
    # Add approval message to existing messages
    messages_for_llm = reverse_messages(state.all_messages + [approval_message])
    
    # Invoke the agent
    result = AGENTS["manual_approver"].invoke({"messages": messages_for_llm})
    
    # Process the result
    messages_result = get_messages(state, result, "manual_approval")
    
    # Return command to update state and go to next node
    return Command(
        update={
            "messages": messages_result["chat_messages"],
            "all_messages": messages_result["all_messages"]
        },
        goto="supervisor",
    )

# Build the graph
builder = StateGraph(CreditState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("background_checker", background_checker_node)
builder.add_node("validate_kyc", validate_kyc_node)
builder.add_node("manual_approver", manual_approver_node)
builder.add_node("credit_score_checker", credit_score_node)
builder.add_node("final_decision", final_decision_node)
builder.add_edge("supervisor", END)

# Compile the graph
graph = builder.compile()
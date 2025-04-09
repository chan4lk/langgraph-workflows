"""
Main workflow graph for the credit approval system.
This module defines the workflow nodes and graph structure with conditional edges.
"""
from typing import Literal
import re
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
from credit_agents_deterministic.prompts import create_agent
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

# Load the language model
LLM = load_chat_model("openai/gpt-4o-mini")

# Create all agents
AGENTS = {
    "credit_score_checker": create_agent("credit_score_checker", LLM, [check_credit_score]),
    "background_checker": create_agent("background_checker", LLM, [perform_background_check]),
    "validate_kyc": create_agent("validate_kyc", LLM, [validate_kyc]),
    "manual_approver": create_agent("manual_approver", LLM, [manual_approval]),
    "final_decision": create_agent("final_decision", LLM, [make_final_decision])
}

def extract_credit_score(state: CreditState) -> int:
    """
    Extracts credit score from the messages in the state.
    
    Args:
        state: Current workflow state
        
    Returns:
        Credit score as an integer or None if not found
    """
    # Default to None if we can't find a credit score
    credit_score = None
    
    # Look through all messages for a credit score
    for message in state.all_messages:
        if hasattr(message, 'content') and isinstance(message.content, str):
            # Look for patterns like "credit score: 720" or "credit score is 720"
            match = re.search(r'credit score(?:\s+is)?(?:\s*:)?\s*(\d+)', message.content.lower())
            if match:
                credit_score = int(match.group(1))
                break
    
    return credit_score

def get_approval_status(state: CreditState) -> bool:
    """
    Checks if the application was approved based on messages.
    
    Args:
        state: Current workflow state
        
    Returns:
        True if approved, False if not approved or status unknown
    """
    for message in state.all_messages:
        if hasattr(message, 'content') and isinstance(message.content, str):
            if 'approved' in message.content.lower() and not 'not approved' in message.content.lower():
                return True
    return False

def has_manual_approval(state: CreditState) -> bool:
    """
    Checks if manual approval has been completed.
    
    Args:
        state: Current workflow state
        
    Returns:
        True if manual approval completed, False otherwise
    """
    for message in state.all_messages:
        if hasattr(message, 'name') and message.name == 'manual_approval':
            return True
    return False

def route_by_credit_score(state: CreditState) -> Literal["credit_score_checker", "background_checker", "validate_kyc", "final_decision"]:
    """
    Routes to the next node based on credit score.
    
    Args:
        state: Current workflow state
        
    Returns:
        Name of the next node
    """
    credit_score = extract_credit_score(state)
    
    # If credit score is unknown, check it
    if credit_score is None:
        return "credit_score_checker"
    
    # Route based on credit score
    if credit_score > 700:
        return "final_decision"
    elif credit_score < 600:
        return "background_checker"
    else:  # Between 600 and 700
        return "validate_kyc"

def route_after_background_check(state: CreditState) -> Literal["manual_approver", "final_decision"]:
    """
    Routes after background check.
    
    Args:
        state: Current workflow state
        
    Returns:
        Name of the next node
    """
    # After background check, go to manual approver
    return "manual_approver"

def route_after_manual_approval(state: CreditState) -> Literal["final_decision"]:
    """
    Routes after manual approval.
    
    Args:
        state: Current workflow state
        
    Returns:
        Name of the next node
    """
    # After manual approval, go to final decision
    return "final_decision"

def route_after_kyc(state: CreditState) -> Literal["manual_approver", "final_decision"]:
    """
    Routes after KYC validation.
    
    Args:
        state: Current workflow state
        
    Returns:
        Name of the next node
    """
    # After KYC validation, go to manual approver
    return "manual_approver"

def is_process_complete(state: CreditState) -> bool:
    """
    Determines if the credit approval process is complete.
    
    Args:
        state: Current workflow state
        
    Returns:
        True if process is complete, False otherwise
    """
    # Check if final decision has been made
    for message in state.all_messages:
        if hasattr(message, 'name') and message.name == 'make_final_decision':
            return True
    
    return False

# Create node handlers with default next nodes
# These will be overridden by conditional edges
credit_score_node = create_node_handler(
    AGENTS["credit_score_checker"], 
    "credit_score_checker"
)

background_checker_node = create_node_handler(
    AGENTS["background_checker"], 
    "background_checker"
)

validate_kyc_node = create_node_handler(
    AGENTS["validate_kyc"], 
    "validate_kyc"
)

final_decision_node = create_node_handler(
    AGENTS["final_decision"], 
    "final_decision"
)

def manual_approver_node(state: CreditState) -> Command:
    """
    Manual approver node that requires user intervention.
    This is a custom node that can't use the standard handler.
    
    Args:
        state: Current workflow state
        
    Returns:
        Command with updated state (next node decided by conditional edge)
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
    
    # Return command to update state (next node decided by conditional edge)
    return Command(
        update={
            "messages": messages_result["chat_messages"],
            "all_messages": messages_result["all_messages"]
        }
    )

# Build the graph with conditional edges
builder = StateGraph(CreditState)

# Add all nodes
builder.add_node("credit_score_checker", credit_score_node)
builder.add_node("background_checker", background_checker_node)
builder.add_node("validate_kyc", validate_kyc_node)
builder.add_node("manual_approver", manual_approver_node)
builder.add_node("final_decision", final_decision_node)

# Add START edge based on credit score
builder.add_conditional_edges(
    START,
    route_by_credit_score,
    {
        "credit_score_checker": "credit_score_checker",
        "background_checker": "background_checker",
        "validate_kyc": "validate_kyc",
        "final_decision": "final_decision"
    }
)

# Add conditional edges from credit_score_checker node
builder.add_conditional_edges(
    "credit_score_checker",
    route_by_credit_score,
    {
        "credit_score_checker": "credit_score_checker",  # Retry if needed
        "background_checker": "background_checker",
        "validate_kyc": "validate_kyc",
        "final_decision": "final_decision"
    }
)

# Add edge from background_checker to manual_approver
builder.add_conditional_edges(
    "background_checker",
    route_after_background_check,
    {
        "manual_approver": "manual_approver",
        "final_decision": "final_decision"
    }
)

# Add edge from validate_kyc to manual_approver
builder.add_conditional_edges(
    "validate_kyc",
    route_after_kyc,
    {
        "manual_approver": "manual_approver",
        "final_decision": "final_decision"
    }
)

# Add edge from manual_approver to final_decision
builder.add_conditional_edges(
    "manual_approver",
    route_after_manual_approval,
    {
        "final_decision": "final_decision"
    }
)

# Add conditional edge from final_decision to END
builder.add_conditional_edges(
    "final_decision",
    is_process_complete,
    {
        True: END,
        False: "credit_score_checker"  # Restart process if not complete
    }
)

# Compile the graph
graph = builder.compile()
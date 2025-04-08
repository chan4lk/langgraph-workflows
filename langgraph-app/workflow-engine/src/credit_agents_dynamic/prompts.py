"""
Prompts and agent creation utilities for the credit approval workflow.
This module centralizes all prompts and agent creation logic to avoid duplication.
"""

from typing import List, Dict, Any, Callable
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel

# System prompts for different agents
SUPERVISOR_PROMPT_TEMPLATE = """
You are a supervisor tasked with managing a conversation between the
following workers: {members}. 
Given the following user request, 
respond with the worker to act next. Each worker will perform a 
task and respond with their results and status. When finished, 
respond with FINISH. If credit score is unknown next worker is credit_score_checker. 
If the credit score is more than 700 next worker is final_decision. 
If the credit score is less than 600 next worker is background_checker. 
If the credit score is between 600 and 700 next worker is validate_kyc.
If manual approval is completed next worker is final_decision.
If the final_decision is Approved next worker is FINISH.
"""

AGENT_PROMPTS = {
    "credit_score_checker": "You are a credit score checker. You need to check the credit score for a CUSTOMER_ID (not application_id). Use the check_credit_score tool with the customer_id.",
    
    "background_checker": "You are a background checker. You need to perform a background check for a CUSTOMER_ID (not application_id). Use the perform_background_check tool with the customer_id.",
    
    "validate_kyc": "You are a KYC validator. You need to validate KYC for a CUSTOMER_ID (not application_id). Use the validate_kyc tool with the customer_id.",
    
    "manual_approver": "You are a manual approver. You need to approve an application. Use the manual_approval tool with the application_id.",
    
    "final_decision": "You are the decision maker. You must make a final decision with a reason such as 'Approved' or 'Rejected'. The credit score must not be exposed. IMPORTANT: You must use the APPLICATION_ID (not customer_id) when calling the make_final_decision tool. The application_id will be provided in the message."
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
    tools: List[BaseTool]
) -> Callable:
    """
    Create an agent with the specified type, LLM, and tools.
    
    Args:
        agent_type: Type of agent to create (must be a key in AGENT_PROMPTS)
        llm: Language model to use
        tools: List of tools for the agent
        
    Returns:
        Created agent
    """
    if agent_type not in AGENT_PROMPTS:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    prompt = AGENT_PROMPTS[agent_type]
    return create_react_agent(llm, tools=tools, prompt=prompt)

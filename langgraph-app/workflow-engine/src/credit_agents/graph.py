from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Union, Any
from typing_extensions import TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
import requests
import json
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

# Define the state for our credit approval workflow
class ApplicationStatus(Enum):
    PENDING = auto()
    CREDIT_CHECK = auto()
    KYC_CHECK = auto()
    INCOME_VERIFICATION = auto()
    BACKGROUND_CHECK = auto()
    MANUAL_APPROVAL = auto()
    FINAL_DECISION = auto()
    APPROVED = auto()
    REJECTED = auto()

class CreditKeys(TypedDict):
    application_id: str
    customer_id: str
    product_type: str
    requested_amount: float
    credit_score: Optional[int]
    kyc_passed: Optional[bool]
    income_verified: Optional[bool]
    background_check_passed: Optional[bool]
    manual_approval_needed: Optional[bool]
    manual_approval_result: Optional[bool]
    final_decision: Optional[str]
    status: ApplicationStatus

@dataclass
class CreditState:
    keys: CreditKeys
    messages: List[Union[HumanMessage, AIMessage]] = field(default_factory=list)

# API Tools for each agent
BASE_URL = "http://localhost:3000"

# Credit Score Checker Agent tools
@tool
def check_credit_score(application_id: str) -> Dict[str, Any]:
    """Check the credit score for a given application"""
    try:
        response = requests.get(f"{BASE_URL}/credit-check", params={"application_id": application_id})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Create a new credit check with a random score between 300 and 850
            import random
            credit_score = random.randint(300, 850)
            response = requests.post(
                f"{BASE_URL}/credit-check", 
                json={"application_id": application_id, "credit_score": credit_score}
            )
            return response.json()
    except Exception as e:
        return {"error": str(e)}

# KYC Validator Agent tools
@tool
def validate_kyc(application_id: str) -> Dict[str, Any]:
    """Validate KYC for a given application"""
    try:
        response = requests.get(f"{BASE_URL}/kyc-check", params={"application_id": application_id})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Create a new KYC check with a random result
            import random
            kyc_passed = random.choice([True, False])
            remarks = "Automated KYC verification" if kyc_passed else "Requires additional documents"
            response = requests.post(
                f"{BASE_URL}/kyc-check", 
                json={"application_id": application_id, "kyc_passed": kyc_passed, "remarks": remarks}
            )
            return response.json()
    except Exception as e:
        return {"error": str(e)}

# Income Verifier Agent tools
@tool
def verify_income(application_id: str) -> Dict[str, Any]:
    """Verify income for a given application"""
    try:
        response = requests.get(f"{BASE_URL}/income-verification", params={"application_id": application_id})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Get the application to determine requested amount
            app_response = requests.get(f"{BASE_URL}/application", params={"id": application_id})
            if app_response.status_code == 200:
                app_data = app_response.json()
                requested_amount = app_data.get("requested_amount", 0)
                # Create a new income verification with a random verified income
                import random
                declared_income = requested_amount * 4  # Assume 4x annual income for loan amount
                variance = random.uniform(0.8, 1.2)  # 20% variance either way
                verified_income = declared_income * variance
                remarks = "Income verification completed"
                response = requests.post(
                    f"{BASE_URL}/income-verification", 
                    json={
                        "application_id": application_id, 
                        "declared_income": declared_income,
                        "verified_income": verified_income,
                        "remarks": remarks
                    }
                )
                return response.json()
            return {"error": "Application not found"}
    except Exception as e:
        return {"error": str(e)}

# Background Check Agent tools
@tool
def perform_background_check(application_id: str) -> Dict[str, Any]:
    """Perform background check for a given application"""
    try:
        response = requests.get(f"{BASE_URL}/background-check", params={"application_id": application_id})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Create a new background check with random results
            import random
            criminal_record = random.choice([True, False])
            debt_collections = random.choice([True, False])
            remarks = "No issues found" if not (criminal_record or debt_collections) else "Issues found"
            response = requests.post(
                f"{BASE_URL}/background-check", 
                json={
                    "application_id": application_id, 
                    "criminal_record": criminal_record,
                    "debt_collections": debt_collections,
                    "remarks": remarks
                }
            )
            return response.json()
    except Exception as e:
        return {"error": str(e)}

# Manual Approver Agent tools
@tool
def manual_approval(application_id: str, approve: bool, notes: str) -> Dict[str, Any]:
    """Perform manual approval for a given application"""
    try:
        # Convert boolean to integer for SQLite compatibility
        approved_int = 1 if approve else 0
        
        response = requests.post(
            f"{BASE_URL}/manual-approval", 
            json={
                "application_id": application_id, 
                "approver_name": "AI Agent",
                "approval_notes": notes,
                "approved": approved_int  # Use integer instead of boolean
            }
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Final Decision Agent tools
@tool
def make_final_decision(application_id: str, decision: str, reason: str) -> Dict[str, Any]:
    """Make the final decision for a given application"""
    try:
        response = requests.post(
            f"{BASE_URL}/final-decision", 
            json={
                "application_id": application_id, 
                "decision": decision,
                "reason": reason
            }
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Agent implementations
def credit_score_checker(state: CreditState) -> CreditState:
    """Agent that checks the credit score"""
    application_id = state.keys.get("application_id")
    result = check_credit_score(application_id)
    
    # Handle None result
    if result is None:
        state.messages.append(AIMessage(content="Error checking credit score: API returned None"))
        # Generate a random credit score as fallback
        import random
        credit_score = random.randint(300, 850)
        state.keys["credit_score"] = credit_score
        state.messages.append(AIMessage(content=f"Generated fallback credit score: {credit_score}"))
        return state
    
    if "error" in result:
        state.messages.append(AIMessage(content=f"Error checking credit score: {result['error']}"))
        # Generate a random credit score as fallback
        import random
        credit_score = random.randint(300, 850)
        state.keys["credit_score"] = credit_score
        state.messages.append(AIMessage(content=f"Generated fallback credit score: {credit_score}"))
        return state
    
    # Ensure credit_score is stored as an integer
    credit_score = int(result.get("credit_score", 0))
    state.keys["credit_score"] = credit_score
    state.messages.append(AIMessage(content=f"Credit score checked: {credit_score}"))
    return state

def kyc_validator(state: CreditState) -> CreditState:
    """Agent that validates KYC"""
    application_id = state.keys.get("application_id")
    result = validate_kyc(application_id)
    
    # Handle None result
    if result is None:
        state.messages.append(AIMessage(content="Error validating KYC: API returned None"))
        # Generate a random KYC result as fallback
        import random
        kyc_passed = random.choice([True, False])
        state.keys["kyc_passed"] = kyc_passed
        state.messages.append(AIMessage(content=f"Generated fallback KYC result: {'Passed' if kyc_passed else 'Failed'}"))
        return state
    
    if "error" in result:
        state.messages.append(AIMessage(content=f"Error validating KYC: {result['error']}"))
        # Generate a random KYC result as fallback
        import random
        kyc_passed = random.choice([True, False])
        state.keys["kyc_passed"] = kyc_passed
        state.messages.append(AIMessage(content=f"Generated fallback KYC result: {'Passed' if kyc_passed else 'Failed'}"))
        return state
    
    kyc_passed = result.get("kyc_passed")
    state.keys["kyc_passed"] = kyc_passed
    state.messages.append(AIMessage(content=f"KYC validation: {'Passed' if kyc_passed else 'Failed'}"))
    return state

def income_verifier(state: CreditState) -> CreditState:
    """Agent that verifies income"""
    application_id = state.keys.get("application_id")
    result = verify_income(application_id)
    
    # Handle None result
    if result is None:
        state.messages.append(AIMessage(content="Error verifying income: API returned None"))
        # Generate a random income verification result as fallback
        import random
        income_verified = random.choice([True, False])
        state.keys["income_verified"] = income_verified
        state.messages.append(AIMessage(content=f"Generated fallback income verification: {'Passed' if income_verified else 'Failed'}"))
        return state
    
    if "error" in result:
        state.messages.append(AIMessage(content=f"Error verifying income: {result['error']}"))
        # Generate a random income verification result as fallback
        import random
        income_verified = random.choice([True, False])
        state.keys["income_verified"] = income_verified
        state.messages.append(AIMessage(content=f"Generated fallback income verification: {'Passed' if income_verified else 'Failed'}"))
        return state
    
    # Convert string values to float for calculation
    declared_income = float(result.get("declared_income", 0))
    verified_income = float(result.get("verified_income", 0))
    
    # Avoid division by zero
    if declared_income > 0:
        income_verified = abs(declared_income - verified_income) / declared_income <= 0.2  # Within 20% tolerance
    else:
        income_verified = False
    
    state.keys["income_verified"] = income_verified
    state.messages.append(AIMessage(content=f"Income verification: {'Passed' if income_verified else 'Failed'}"))
    return state

def background_checker(state: CreditState) -> CreditState:
    """Agent that performs background checks"""
    application_id = state.keys.get("application_id")
    result = perform_background_check(application_id)
    
    # Handle None result
    if result is None:
        state.messages.append(AIMessage(content="Error performing background check: API returned None"))
        # Generate a random background check result as fallback
        import random
        background_check_passed = random.choice([True, False])
        state.keys["background_check_passed"] = background_check_passed
        state.messages.append(AIMessage(content=f"Generated fallback background check: {'Passed' if background_check_passed else 'Failed'}"))
        return state
    
    if "error" in result:
        state.messages.append(AIMessage(content=f"Error performing background check: {result['error']}"))
        # Generate a random background check result as fallback
        import random
        background_check_passed = random.choice([True, False])
        state.keys["background_check_passed"] = background_check_passed
        state.messages.append(AIMessage(content=f"Generated fallback background check: {'Passed' if background_check_passed else 'Failed'}"))
        return state
    
    criminal_record = result.get("criminal_record")
    debt_collections = result.get("debt_collections")
    background_check_passed = not (criminal_record or debt_collections)
    
    state.keys["background_check_passed"] = background_check_passed
    state.messages.append(AIMessage(content=f"Background check: {'Passed' if background_check_passed else 'Failed'}"))
    return state

def manual_approver(state: CreditState) -> CreditState:
    """Agent that handles manual approval"""
    application_id = state.keys.get("application_id")
    
    # Make a decision based on the available information
    credit_score = state.keys.get("credit_score", 0)
    kyc_passed = state.keys.get("kyc_passed", False)
    income_verified = state.keys.get("income_verified", False)
    background_check_passed = state.keys.get("background_check_passed", False)
    
    # Logic for manual approval
    approve = False
    notes = ""
    
    if credit_score >= 600 and kyc_passed and income_verified:
        approve = True
        notes = "Approved based on good credit score, passed KYC, and verified income despite background issues."
    elif credit_score >= 700 and kyc_passed:
        approve = True
        notes = "Approved based on excellent credit score and passed KYC despite income verification issues."
    else:
        approve = False
        notes = "Rejected due to combination of issues with credit score, KYC, income verification, or background check."
    
    # Call the tool with a single argument (dict)
    result = manual_approval({"application_id": application_id, "approve": approve, "notes": notes})
    
    # Handle None result
    if result is None:
        state.messages.append(AIMessage(content="Error in manual approval: API returned None"))
        # Use the decision we already made
        state.keys["manual_approval_result"] = approve
        state.messages.append(AIMessage(content=f"Manual approval (local decision): {'Approved' if approve else 'Rejected'} - {notes}"))
        return state
    
    if "error" in result:
        state.messages.append(AIMessage(content=f"Error in manual approval: {result['error']}"))
        # Use the decision we already made
        state.keys["manual_approval_result"] = approve
        state.messages.append(AIMessage(content=f"Manual approval (local decision): {'Approved' if approve else 'Rejected'} - {notes}"))
        return state
    
    state.keys["manual_approval_result"] = approve
    state.messages.append(AIMessage(content=f"Manual approval: {'Approved' if approve else 'Rejected'} - {notes}"))
    return state

def final_decision_maker(state: CreditState) -> CreditState:
    """Agent that makes the final decision"""
    application_id = state.keys.get("application_id")
    
    # Gather all information for decision making
    credit_score = state.keys.get("credit_score", 0)
    kyc_passed = state.keys.get("kyc_passed", False)
    income_verified = state.keys.get("income_verified", False)
    background_check_passed = state.keys.get("background_check_passed", False)
    manual_approval_result = state.keys.get("manual_approval_result")
    
    # Final decision logic
    decision = "Rejected"
    reason = ""
    
    # Automatic approval path
    if credit_score >= 700 and kyc_passed and income_verified and background_check_passed:
        decision = "Approved"
        reason = "All checks passed with excellent credit score."
    # Manual approval path
    elif manual_approval_result is not None:
        decision = "Approved" if manual_approval_result else "Rejected"
        reason = f"Based on manual review: {'Approved' if manual_approval_result else 'Rejected'}"
    # Automatic rejection path
    else:
        decision = "Rejected"
        reason = "Failed to meet automatic approval criteria and manual approval was not favorable."
    
    # Call the tool with a single argument (dict)
    result = make_final_decision({"application_id": application_id, "decision": decision, "reason": reason})
    
    # Handle None result
    if result is None:
        state.messages.append(AIMessage(content="Error in final decision: API returned None"))
        # Use the decision we already made
        state.keys["final_decision"] = decision
        state.messages.append(AIMessage(content=f"Final decision (local): {decision} - {reason}"))
        # Update the application status
        state.keys["status"] = ApplicationStatus.APPROVED if decision == "Approved" else ApplicationStatus.REJECTED
        return state
    
    if "error" in result:
        state.messages.append(AIMessage(content=f"Error in final decision: {result['error']}"))
        # Use the decision we already made
        state.keys["final_decision"] = decision
        state.messages.append(AIMessage(content=f"Final decision (local): {decision} - {reason}"))
        # Update the application status
        state.keys["status"] = ApplicationStatus.APPROVED if decision == "Approved" else ApplicationStatus.REJECTED
        return state
    
    state.keys["final_decision"] = decision
    state.messages.append(AIMessage(content=f"Final decision: {decision} - {reason}"))
    
    # Update the application status
    state.keys["status"] = ApplicationStatus.APPROVED if decision == "Approved" else ApplicationStatus.REJECTED
    
    return state

# Update state after each agent completes
def update_status(state: CreditState) -> CreditState:
    """Update the application status based on the last agent that ran"""
    last_message = state.messages[-1] if state.messages else None
    
    if not last_message:
        return state
    
    content = last_message.content.lower()
    
    if "credit score checked" in content:
        state.keys["status"] = ApplicationStatus.CREDIT_CHECK
    elif "kyc validation" in content:
        state.keys["status"] = ApplicationStatus.KYC_CHECK
    elif "income verification" in content:
        state.keys["status"] = ApplicationStatus.INCOME_VERIFICATION
    elif "background check" in content:
        state.keys["status"] = ApplicationStatus.BACKGROUND_CHECK
    elif "manual approval" in content:
        state.keys["status"] = ApplicationStatus.MANUAL_APPROVAL
    elif "final decision" in content:
        if "approved" in content:
            state.keys["status"] = ApplicationStatus.APPROVED
        else:
            state.keys["status"] = ApplicationStatus.REJECTED
    
    return state

# Create the workflow graph
def create_credit_approval_workflow():
    """Create the credit approval workflow graph"""
    # Create a new graph
    workflow = StateGraph(CreditState)
    
    # Add nodes for each agent
    workflow.add_node("credit_score_checker", credit_score_checker)
    workflow.add_node("kyc_validator", kyc_validator)
    workflow.add_node("income_verifier", income_verifier)
    workflow.add_node("background_checker", background_checker)
    workflow.add_node("manual_approver", manual_approver)
    workflow.add_node("final_decision_maker", final_decision_maker)
    workflow.add_node("status_updater", update_status)
    
    # Add edges for the standard flow
    workflow.add_edge("credit_score_checker", "status_updater")
    workflow.add_edge("kyc_validator", "status_updater")
    workflow.add_edge("income_verifier", "status_updater")
    workflow.add_edge("background_checker", "status_updater")
    workflow.add_edge("manual_approver", "status_updater")
    workflow.add_edge("final_decision_maker", "status_updater")
    
    # Define routing logic after status update
    def route_after_status_update(state):
        status = state.keys.get("status", ApplicationStatus.PENDING)
        
        if status == ApplicationStatus.CREDIT_CHECK:
            return "kyc_validator"
        elif status == ApplicationStatus.KYC_CHECK:
            return "income_verifier"
        elif status == ApplicationStatus.INCOME_VERIFICATION:
            # Check if background check is needed
            # Convert credit_score to int for comparison
            credit_score = int(state.keys.get("credit_score", 0))
            if credit_score < 650:
                return "background_checker"
                
            # Check if manual approval is needed
            kyc_passed = state.keys.get("kyc_passed", False)
            income_verified = state.keys.get("income_verified", False)
            if credit_score >= 600 and (not kyc_passed or not income_verified):
                return "manual_approver"
                
            return "final_decision_maker"
        elif status == ApplicationStatus.BACKGROUND_CHECK:
            # Check if manual approval is needed
            # Convert credit_score to int for comparison
            credit_score = int(state.keys.get("credit_score", 0))
            kyc_passed = state.keys.get("kyc_passed", False)
            income_verified = state.keys.get("income_verified", False)
            background_check_passed = state.keys.get("background_check_passed", False)
            
            if credit_score >= 600 and (not kyc_passed or not income_verified or not background_check_passed):
                return "manual_approver"
                
            return "final_decision_maker"
        elif status == ApplicationStatus.MANUAL_APPROVAL:
            return "final_decision_maker"
        elif status in [ApplicationStatus.APPROVED, ApplicationStatus.REJECTED]:
            return END
        else:
            # Default for PENDING status
            return "credit_score_checker"
    
    # Add conditional edges from status updater
    workflow.add_conditional_edges(
        "status_updater",
        route_after_status_update,
        {
            "credit_score_checker": "credit_score_checker",
            "kyc_validator": "kyc_validator",
            "income_verifier": "income_verifier",
            "background_checker": "background_checker",
            "manual_approver": "manual_approver",
            "final_decision_maker": "final_decision_maker",
            END: END
        }
    )
    
    # Set the entry point
    workflow.set_entry_point("status_updater")
    
    return workflow.compile()

# Create the workflow
graph = create_credit_approval_workflow()

# Example usage
def process_application(application_id: str, customer_id: str, product_type: str, requested_amount: float):
    """Process a credit application through the workflow"""
    # Initialize the state
    initial_state = CreditState(
        keys={
            "application_id": application_id,
            "customer_id": customer_id,
            "product_type": product_type,
            "requested_amount": requested_amount,
            "status": ApplicationStatus.PENDING
        }
    )
    
    # Run the workflow
    result = graph.invoke(initial_state)
    
    return result

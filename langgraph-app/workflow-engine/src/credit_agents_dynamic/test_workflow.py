from credit_agents_dynamic.graph import graph
from credit_agents_dynamic.state import CreditState, CreditKeys, ApplicationStatus
from langchain_core.messages import HumanMessage
import uuid

def test_credit_workflow():
    # Create initial application data
    application_id = str(uuid.uuid4())
    customer_id = "CUST-" + str(uuid.uuid4())[:8]
    
    # Initialize the state with required keys
    initial_state = CreditState(
        keys=CreditKeys(
            application_id=application_id,
            customer_id=customer_id,
            product_type="Personal Loan",
            requested_amount=10000.0,
            credit_score=None,  # Will be determined by the credit_score_checker
            kyc_passed=None,
            income_verified=None,
            background_check_passed=None,
            manual_approval_needed=None,
            manual_approval_result=None,
            final_decision=None,
            status=ApplicationStatus.PENDING
        )
    )
    
    # Add an initial message to the state
    initial_message = HumanMessage(
        content=f"Process credit application with ID: {application_id} for customer: {customer_id}. "
                f"Product type: Personal Loan, requested amount: $10,000."
    )
    initial_state.messages.append(initial_message)
    
    # Run the workflow
    for output in graph.stream(initial_state):
        print(f"Step: {output.get('next', 'unknown')}")
        
    # Get the final state
    final_state = output
    
    # Print the final decision
    print(f"\nFinal Decision: {final_state['keys'].get('final_decision', 'No decision')}")
    print(f"Application Status: {final_state['keys'].get('status', 'Unknown')}")
    
    return final_state

if __name__ == "__main__":
    test_credit_workflow()

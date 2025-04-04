from credit_agents_dynamic.graph import graph
from credit_agents_dynamic.state import CreditState
from langchain_core.messages import HumanMessage

import dotenv

dotenv.load_dotenv()

def run_workflow(application_id, customer_id, product_type, amount, auto_approve=True):
    """Helper function to run the workflow with different parameters"""
    # Initialize the state
    initial_state = CreditState()
    
    # Add the initial message to the state
    initial_message = HumanMessage(
        content=f"Process credit application with ID: {application_id} for customer: {customer_id}. "
                f"Product type: {product_type}, requested amount: ${amount}."
    )
    initial_state.messages.append(initial_message)
    
    # Run the workflow and track the steps
    print(f"\nStarting credit application workflow for {application_id} ({customer_id})...\n")
    print(f"Initial request: Process credit application with ID: {application_id} for customer: {customer_id}")
    print(f"Product type: {product_type}, requested amount: ${amount}")
    print("\nWorkflow execution:")
    
    # Mock the interrupt response
    from unittest.mock import patch
    
    with patch('langgraph.types.interrupt', return_value=auto_approve):
        # Run the workflow
        for i, output in enumerate(graph.stream(initial_state)):
            print(f"Step {i+1}:")
            
            # For debugging, print the output keys
            if i == 0:
                print(f"Output keys: {list(output.keys()) if isinstance(output, dict) else 'Not a dict'}")
            
            # Just print the raw API responses that we can see
            if 'Checking credit score' in str(output):
                print("Credit score check executed")
            if 'background check' in str(output).lower():
                print("Background check executed")
            if 'kyc' in str(output).lower():
                print("KYC validation executed")
            if 'manual approval' in str(output).lower():
                print(f"Manual approval executed (Decision: {'Approved' if auto_approve else 'Rejected'})")
            if 'final decision' in str(output).lower():
                print("Final decision executed")
            
            print("---")
    
    # Get the final state
    final_state = output
    
    # Print workflow summary
    print(f"\nSummary for {application_id}:")
    print(f"Application ID: {application_id}")
    print(f"Customer ID: {customer_id}")
    print(f"Product type: {product_type}")
    print(f"Amount requested: ${amount}")
    print(f"Manual approval decision: {'Approved' if auto_approve else 'Rejected'}")
    
    # Return the final state
    return output

def test_specific_credit_application():
    """Test processing a specific credit application with ID: APP001 for customer: CUST001"""
    return run_workflow("APP001", "CUST001", "credit_card", 5000)

def test_low_credit_score_application():
    """Test processing an application with low credit score (APP002)"""
    # This will test the path where credit score is low and background check is needed
    # Auto-approve is set to True for the manual approval step
    return run_workflow("APP002", "CUST002", "personal_loan", 15000, auto_approve=True)

def test_medium_credit_score_application():
    """Test processing an application with medium credit score and KYC issues (APP003)"""
    # This will test the path where credit score is medium and KYC validation is needed
    # Auto-approve is set to False to test rejection in the manual approval step
    return run_workflow("APP003", "CUST003", "mortgage", 250000, auto_approve=False)
    
    return final_state

def test_random_credit_application():
    """Test with random application and customer IDs"""
    import uuid
    
    # Create random IDs
    application_id = str(uuid.uuid4())
    customer_id = "CUST-" + str(uuid.uuid4())[:8]
    
    return run_workflow(application_id, customer_id, "Personal Loan", 10000)

if __name__ == "__main__":
    print("\n===== TEST CASE 1: High Credit Score Application =====\n")
    test_specific_credit_application()
    
    print("\n\n===== TEST CASE 2: Low Credit Score Application with Approval =====\n")
    test_low_credit_score_application()
    
    print("\n\n===== TEST CASE 3: Medium Credit Score Application with Rejection =====\n")
    test_medium_credit_score_application()

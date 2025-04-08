"""Test script for the credit approval workflow.

This module contains functions to test the credit approval workflow with different scenarios.
"""

import dotenv
from unittest.mock import patch
from langchain_core.messages import HumanMessage

from credit_agents_deterministic.graph import graph
from credit_agents_deterministic.state import CreditState

# Load environment variables
dotenv.load_dotenv()

def run_workflow(application_id, customer_id, product_type, amount, auto_approve=True):
    """Helper function to run the workflow with different parameters
    
    Args:
        application_id: ID of the credit application
        customer_id: ID of the customer
        product_type: Type of product (e.g., credit_card, mortgage)
        amount: Amount requested
        auto_approve: Whether to automatically approve the application in manual approval step
        
    Returns:
        Final state of the workflow
    """
    # Initialize the state
    initial_state = CreditState() 
    
    # Add the initial message to the state
    initial_message = HumanMessage(
        content=f"Process credit application with ID: {application_id} for customer: {customer_id}. "
                f"Product type: {product_type}, requested amount: ${amount}."
    )
    initial_state.messages.append(initial_message)
    
    # Print workflow information
    print(f"\nStarting credit application workflow for {application_id} ({customer_id})...\n")
    print(f"Initial request: Process credit application with ID: {application_id} for customer: {customer_id}")
    print(f"Product type: {product_type}, requested amount: ${amount}")
    print("\nWorkflow execution:")
    
    # Mock the interrupt function to return auto_approve
    with patch('credit_agents_dynamic.graph.interrupt', return_value=auto_approve):
        # Run the workflow and track steps
        for i, output in enumerate(graph.stream(initial_state)):
            print(f"Step {i+1}:")
            
            # For debugging, print the output keys on first step
            if i == 0:
                print(f"Output keys: {list(output.keys()) if isinstance(output, dict) else 'Not a dict'}")
            
            # Print information about which step is executing
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
    """Test processing a specific credit application with high credit score
    
    Application ID: APP001, Customer ID: CUST001
    Product: Credit Card, Amount: $5,000
    Expected path: credit_score_checker -> final_decision
    """
    return run_workflow("APP001", "CUST001", "credit_card", 5000)

def test_low_credit_score_application():
    """Test processing an application with low credit score
    
    Application ID: APP002, Customer ID: CUST002
    Product: Personal Loan, Amount: $10,000
    Expected path: credit_score_checker -> background_checker -> manual_approver -> final_decision
    """
    return run_workflow("APP002", "CUST002", "personal_loan", 10000)

def test_medium_credit_score_application():
    """Test processing an application with medium credit score
    
    Application ID: APP003, Customer ID: CUST003
    Product: Mortgage, Amount: $250,000
    Expected path: credit_score_checker -> validate_kyc -> manual_approver -> final_decision
    Auto-approve is set to False to test rejection in the manual approval step
    """
    return run_workflow("APP003", "CUST003", "mortgage", 250000, auto_approve=False)

def test_random_credit_application():
    """Test with random application and customer IDs
    
    Generates random application and customer IDs
    Product: Credit Card, Amount: Random between $1,000 and $10,000
    """
    import random
    import string
    
    # Generate random IDs
    app_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    cust_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    amount = random.randint(1000, 10000)
    
    print(f"\nRandom test with:\nApplication ID: {app_id}\nCustomer ID: {cust_id}\nAmount: ${amount}")
    
    # Run with random parameters
    return run_workflow(app_id, cust_id, "credit_card", amount)

if __name__ == "__main__":
    print("\n===== TEST CASE 1: High Credit Score Application =====\n")
    test_specific_credit_application()
    # test_low_credit_score_application()
    
    # print("\n\n===== TEST CASE 3: Medium Credit Score Application with Rejection =====\n")
    # test_medium_credit_score_application()

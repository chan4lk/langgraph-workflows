import sys
import os
import json
from pprint import pprint

# Add the parent directory to sys.path to import the graph module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.credit_agents.graph import process_application, ApplicationStatus

def test_credit_approval_workflow():
    """Test the credit approval workflow with a sample application"""
    print("Testing Credit Approval Workflow")
    print("===============================")
    
    # Sample application data
    application_id = "APP123456"
    customer_id = "CUST789012"
    product_type = "credit_card"
    requested_amount = 5000.0
    
    print(f"Processing application {application_id} for customer {customer_id}")
    print(f"Product: {product_type}, Requested Amount: ${requested_amount}")
    print("\nWorkflow Execution:")
    print("------------------")
    
    # Process the application through the workflow
    result = process_application(
        application_id=application_id,
        customer_id=customer_id,
        product_type=product_type,
        requested_amount=requested_amount
    )
    
    # Extract and display messages from the workflow
    messages = result.messages
    for i, message in enumerate(messages):
        print(f"Step {i+1}: {message.content}")
    
    # Display final state
    print("\nFinal Application State:")
    print("----------------------")
    
    # Convert Enum to string for better readability
    state_dict = {k: (v.name if isinstance(v, ApplicationStatus) else v) for k, v in result.keys.items()}
    pprint(state_dict)
    
    # Display final decision
    final_decision = result.keys.get("final_decision", "Unknown")
    print(f"\nFinal Decision: {final_decision}")
    
    return result

if __name__ == "__main__":
    test_credit_approval_workflow()

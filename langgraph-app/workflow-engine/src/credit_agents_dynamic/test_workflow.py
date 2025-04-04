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
    
    # Mock the interrupt response
    from unittest.mock import patch
    
    # Create a list to store all messages from each step
    all_messages = []
    
    with patch('langgraph.types.interrupt', return_value=auto_approve):
        # Run the workflow
        for i, output in enumerate(graph.stream(initial_state)):
            # Print step number
            print(f"Step {i+1}:")
            
            # Check for new messages
            if output.get('messages'):
                # Get only new messages that weren't in previous steps
                new_messages = output.get('messages')[len(all_messages):] if all_messages else output.get('messages')
                all_messages = output.get('messages')
                
                # Print new messages
                for msg in new_messages:
                    if hasattr(msg, 'content'):
                        name = getattr(msg, 'name', 'user' if hasattr(msg, 'type') and msg.type == 'human' else 'System')
                        content = msg.content
                        print(f"[{name}]: {content[:100]}..." if len(content) > 100 else f"[{name}]: {content}")
            print("---")
    
    # Get the final state
    final_state = output
    
    # Print workflow summary
    print(f"\nWorkflow Summary for {application_id}:")
    
    # Get the final state
    final_state = output
    
    # Print all messages in the conversation
    print("\nFull Conversation History:")
    agent_sequence = []
    
    for i, msg in enumerate(final_state.get('messages', [])):
        # Determine message name/sender
        if hasattr(msg, 'name') and msg.name:
            name = msg.name
            # Track agent sequence
            if name not in ['user', 'System'] and name not in agent_sequence:
                agent_sequence.append(name)
        elif hasattr(msg, 'type') and msg.type == 'human':
            name = 'user'
        else:
            name = 'System'
            
        # Print message
        if hasattr(msg, 'content'):
            content = msg.content
            print(f"[{i+1}] {name}: {content[:100]}..." if len(content) > 100 else f"[{i+1}] {name}: {content}")
    
    # Print agent sequence
    if agent_sequence:
        print("\nAgent execution sequence:")
        print(" -> ".join(agent_sequence))
    
    return final_state

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

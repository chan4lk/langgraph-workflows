from credit_agents_dynamic.graph import graph
from credit_agents_dynamic.state import CreditState
from langchain_core.messages import HumanMessage

import dotenv

dotenv.load_dotenv()

def test_specific_credit_application():
    """Test processing a specific credit application with ID: APP001 for customer: CUST001"""
    # Initialize the state
    initial_state = CreditState()
    
    # Add the initial message to the state with the specific application and customer IDs
    initial_message = HumanMessage(
        content="Process credit application with ID: APP001 for customer: CUST001. "
                "Product type: credit_card, requested amount: $5,000."
    )
    initial_state.messages.append(initial_message)
    
    # Run the workflow and track the steps
    print("Starting credit application workflow for APP001 (CUST001)...\n")
    steps = []
    
    for output in graph.stream(initial_state):
        current_step = output.get('next', 'unknown')
        steps.append(current_step)
        print(f"Step: {current_step}")
        
        # Print the latest message if available
        if output.get('messages') and len(output['messages']) > 0:
            latest_message = output['messages'][-1]
            if hasattr(latest_message, 'content'):
                print(f"Message: {latest_message.content[:100]}..." if len(latest_message.content) > 100 else f"Message: {latest_message.content}")
        print("---")
    
    # Get the final state
    final_state = output
    
    # Print workflow summary
    print("\nWorkflow Summary:")
    print(f"Total steps: {len(steps)}")
    print(f"Step sequence: {' -> '.join(steps)}")
    
    # Print all messages in the conversation
    print("\nConversation History:")
    for i, msg in enumerate(final_state.get('messages', [])):
        name = getattr(msg, 'name', 'System')
        print(f"[{i+1}] {name}: {msg.content[:50]}..." if len(msg.content) > 50 else f"[{i+1}] {name}: {msg.content}")
    
    return final_state

def test_credit_workflow():
    """Test with random application and customer IDs"""
    import uuid
    
    # Create random IDs
    application_id = str(uuid.uuid4())
    customer_id = "CUST-" + str(uuid.uuid4())[:8]
    
    # Initialize the state
    initial_state = CreditState()
    
    # Add the initial message to the state
    initial_message = HumanMessage(
        content=f"Process credit application with ID: {application_id} for customer: {customer_id}. "
                f"Product type: Personal Loan, requested amount: $10,000."
    )
    initial_state.messages.append(initial_message)
    
    # Run the workflow
    for output in graph.stream(initial_state):
        print(f"Step: {output.get('next', 'unknown')}")
    
    return output

if __name__ == "__main__":
    test_specific_credit_application()

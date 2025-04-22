from langgraph.graph import StateGraph, START, END
from typing import Dict, Any, cast
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
# Import our modular components
from bookstore.types import BookstoreState 
from bookstore.agents import book_info_provider, catalog_updater, supervisor

# Create the workflow graph
def create_bookstore_graph() -> StateGraph:
    """
    Creates and configures the bookstore workflow graph.
    
    Returns:
        Configured StateGraph for the bookstore workflow
    """
    # Initialize the graph with our state type
    builder = StateGraph(BookstoreState)
    
    # Add the nodes to the graph
    builder.add_node("book_info_provider", book_info_provider)
    builder.add_node("catalog_updater", catalog_updater)
    builder.add_node("supervisor", supervisor)
    
    # Set up the edges
    builder.add_edge(START, "supervisor")
    builder.add_edge("supervisor", END)
    builder.add_edge("book_info_provider", "supervisor")
    builder.add_edge("catalog_updater", "supervisor")
    
    # Compile the graph
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

# Function to process a user request through the workflow
def process_request(user_request: str) -> Dict[str, Any]:
    """
    Processes a user request through the bookstore workflow.
    
    Args:
        user_request: The user's request string
        
    Returns:
        Final state after processing the request
    """
    # Create the graph
    bookstore_graph = create_bookstore_graph()
    
    # Create a human message from the user request
    human_message = HumanMessage(content=user_request)
    messages = [human_message]
    
    # Initialize the state
    initial_state = BookstoreState(
        messages=messages
    )
    
    # Run the workflow
    result = bookstore_graph.invoke(initial_state)
    
    # Return the final state keys and messages
    return {
        "state": dict(result.keys),
        "messages": [m.content for m in result.messages if hasattr(m, 'content')]
    }

# Example usage
if __name__ == "__main__":
    # Example request for finding book information
    info_request = "Can you find information about 'The Great Gatsby'?"
    info_result = process_request(info_request)
    print(f"Book Info Request Result: {info_result['messages'][-1] if info_result['messages'] else 'No response'}")
    
    # Example request for updating the catalog
    update_request = "Please add a new book 'Python Programming' to the catalog"
    update_result = process_request(update_request)
    print(f"Catalog Update Request Result: {update_result['messages'][-1] if update_result['messages'] else 'No response'}")

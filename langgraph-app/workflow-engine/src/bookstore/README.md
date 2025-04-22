# Bookstore LangGraph Workflow

This module implements a LangGraph workflow for a bookstore with three specialized agents:

1. **Supervisor (Router)** - Routes requests to the appropriate agent based on the user's query
2. **Book Info Provider** - Retrieves information about books
3. **Book Catalog Updater** - Updates the bookstore catalog with new books

## Architecture

The workflow uses a dataclass-based state management approach:

- `BookstoreState` dataclass holds the workflow state
- `BookstoreKeys` TypedDict defines the structure of state keys
- Agents are implemented as functions that process specific parts of the workflow
- The supervisor routes between agents based on the content of the user request

## Components

- `types.py` - Contains state definitions and types
- `agents.py` - Contains implementations of the three agents
- `graph.py` - Defines the workflow graph structure and execution logic

## Usage Example

```python
from bookstore.graph import process_request

# Example request for finding book information
info_request = "Can you find information about 'The Great Gatsby'?"
info_result = process_request(info_request)
print(f"Book Info Request Result: {info_result}")

# Example request for updating the catalog
update_request = "Please add a new book 'Python Programming' to the catalog"
update_result = process_request(update_request)
print(f"Catalog Update Request Result: {update_result}")
```

## Extending the Workflow

To extend this workflow:

1. Add additional state fields to `BookstoreKeys` in `types.py`
2. Implement new agent functions in `agents.py`
3. Update the supervisor logic to route to your new agents
4. Add new nodes to the graph in `create_bookstore_graph()`

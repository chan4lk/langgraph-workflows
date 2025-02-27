# LangGraph Slack Lead Processing Application

A modular, SDK-based workflow for processing Slack leads with intelligent routing and manual approval.

## Project Structure

The project is organized into two main components:

1. **Workflow Engine**: Contains the LangGraph workflow for processing leads from Slack
2. **API**: FastAPI application that provides endpoints for interacting with the workflow

```
langgraph-app/
├── api/                  # FastAPI application
│   ├── main.py           # API endpoints
│   ├── client.py         # Test client
│   ├── requirements.txt  # API dependencies
│   └── README.md         # API documentation
├── workflow-engine/      # LangGraph workflow
│   ├── src/              # Source code
│   │   └── slack_approval/  # Slack lead processing workflow
│   │       ├── __init__.py
│   │       ├── graph.py     # Workflow graph
│   │       ├── nodes.py     # Workflow nodes
│   │       ├── state.py     # Workflow state
│   │       └── utils.py     # Utility functions
│   ├── start_server.py   # Server startup script
│   ├── pyproject.toml    # Package configuration
│   ├── requirements.txt  # Workflow dependencies
│   └── README.md         # Workflow documentation
└── README.md             # Project documentation
```

## Features

- **Lead Extraction**: Extract key lead attributes (geo_location, industry, engagement)
- **Intelligent Routing**: Dynamically assign sales persons based on lead characteristics
- **Manual Approval**: Implement approval mechanism for lead assignments
- **Hubspot Integration**: Create leads in Hubspot after approval
- **Notification**: Notify assigned sales persons

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Install the workflow engine:

```bash
cd workflow-engine
pip install -e .
```

2. Install the API dependencies:

```bash
cd ../api
pip install -r requirements.txt
```

### Running the Application

1. Start the LangGraph server:

```bash
cd workflow-engine
python start_server.py
```

This will start a server on http://localhost:2024 that exposes the Slack lead processing workflow as an API.

2. In a new terminal, start the API server:

```bash
cd api
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

3. Test the application using the client script:

```bash
cd api
python client.py
```

## API Endpoints

- `POST /api/slack/lead`: Process a lead from Slack
- `POST /api/slack/approve`: Approve or reject a lead assignment
- `GET /api/slack/thread/{thread_id}`: Get the status of a workflow thread

## Workflow Steps

1. **Extract Lead Info**: Extract key information from the Slack message
2. **Assign Sales Person**: Assign a sales person based on the lead attributes
3. **Send Approval Request**: Pause the workflow and wait for approval
4. **Create Hubspot Lead**: Create a lead in Hubspot (if approved)
5. **Notify Sales Person**: Notify the assigned sales person (if approved)

## Architecture

The application uses a modular architecture with the following components:

- **LangGraph Workflow**: Defines the workflow structure and transitions
- **FastAPI Application**: Provides endpoints for interacting with the workflow
- **LangGraph SDK**: Connects the API to the LangGraph server

## Development

To develop and extend the application:

1. Make changes to the workflow components in the `workflow-engine/src/slack_approval` directory
2. Start the LangGraph server to test your changes
3. Make changes to the API in the `api` directory
4. Start the API server to test your changes
5. Use the client script to test the full application

## Error Handling

The application includes error handling for common issues, such as:

- Invalid input data
- Missing lead attributes
- Approval rejection
- LangGraph server errors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Slack Lead Processing Workflow

This package contains the LangGraph workflow for processing leads from Slack. It extracts lead information, assigns sales persons, and handles the approval process.

## Overview

The Slack lead processing workflow is designed to automate the process of handling leads that come in through Slack. It uses LangGraph to create a modular, intelligent workflow that can extract key information from Slack messages, assign appropriate sales persons, and manage the approval process.

## Features

- Extract lead attributes (geo_location, industry, engagement) from Slack messages
- Dynamically assign sales persons based on lead characteristics
- Implement manual approval mechanism
- Create Hubspot leads after approval
- Notify assigned sales persons

## Components

The workflow is composed of the following components:

- **Graph**: Defines the workflow structure and transitions
- **Nodes**: Implement the individual steps of the workflow
- **State**: Manages the workflow state and data
- **Utils**: Provides utility functions for the workflow

## Running the Server

To start the LangGraph server:

```bash
python start_server.py
```

This will start a server on http://localhost:2024 that exposes the Slack lead processing workflow as an API.

## Integration with FastAPI

The workflow is designed to be used with the FastAPI application in the `api` directory. The API connects to the LangGraph server using the LangGraph SDK and provides endpoints for processing leads, approving assignments, and checking workflow status.

## Configuration

The workflow can be configured by modifying the following files:

- `src/slack_approval/graph.py`: Define the workflow structure and transitions
- `src/slack_approval/nodes.py`: Implement the workflow steps
- `src/slack_approval/state.py`: Define the workflow state
- `src/slack_approval/utils.py`: Provide utility functions

## Workflow Steps

1. **Extract Lead Info**: Extract key information from the Slack message
2. **Assign Sales Person**: Assign a sales person based on the lead attributes
3. **Send Approval Request**: Pause the workflow and wait for approval
4. **Create Hubspot Lead**: Create a lead in Hubspot (if approved)
5. **Notify Sales Person**: Notify the assigned sales person (if approved)

## Error Handling

The workflow includes error handling for common issues, such as:

- Invalid input data
- Missing lead attributes
- Approval rejection

## Development

To develop and extend the workflow:

1. Install the package in development mode:
   ```
   pip install -e .
   ```

2. Make changes to the workflow components
3. Start the server to test your changes
4. Use the API to interact with the workflow
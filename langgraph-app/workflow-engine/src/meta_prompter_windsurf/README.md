# Meta Prompter Windsurf Workflow

A LangGraph workflow for generating Windsurf prompts for architecture definition, app building, and UI automation with Playwright.

## Overview

This workflow takes an app idea as input and generates a series of prompts for:

1. Requirements analysis
2. UI flow generation
3. UI prompt generation
4. Architecture prompt generation
5. Tech stack selection (with human-in-the-loop)
6. App building prompt generation
7. UI automation prompt generation

## Features

- **Modular Architecture**: Organized into separate modules for types, prompts, parsers, nodes, and utilities
- **Human-in-the-Loop**: Interactive workflow that pauses for human input during tech stack selection
- **Robust Error Handling**: Fallback mechanisms for JSON parsing and message handling
- **Streaming Support**: Stream workflow events for real-time UI updates

## Directory Structure

```
meta_prompter_windsurf/
├── __init__.py                # Package exports
├── graph.py                   # Main workflow graph definition
├── messages.py                # Message handling utilities
├── nodes/                     # Node functions
│   ├── __init__.py
│   └── workflow_nodes.py      # Implementation of workflow steps
├── parsers/                   # Output parsers
│   ├── __init__.py
│   └── output_parsers.py      # JSON and fallback parsers
├── prompts/                   # Prompt templates
│   ├── __init__.py
│   └── templates.py           # LLM prompt definitions
├── types/                     # Type definitions
│   ├── __init__.py
│   └── agent_state.py         # AgentState dataclass
└── utils/                     # Utility functions
    ├── __init__.py
    └── helpers.py             # Helper functions
```

## Usage

### Non-Interactive Mode

```python
from meta_prompter_windsurf import run_meta_prompter

# Run the workflow with an app idea
app_idea = "A task management app that helps users organize their daily tasks."
result = run_meta_prompter(app_idea)

# Access the results
print(f"Requirements: {result['requirements']}")
print(f"UI Flows: {result['ui_flows']}")
print(f"Architecture Prompts: {result['architecture_prompts']}")
print(f"Tech Stack Choice: {result['tech_stack_choice']}")
print(f"App Building Prompts: {result['app_building_prompts']}")
print(f"UI Automation Prompts: {result['ui_automation_prompts']}")
```

### Interactive Mode (Human-in-the-Loop)

```python
from meta_prompter_windsurf import run_meta_prompter_interactive, continue_workflow_with_input

# Start the workflow
app_idea = "A recipe sharing platform where users can upload and search recipes."
events, state, human_input_required = run_meta_prompter_interactive(app_idea)

if human_input_required:
    # Get human input for tech stack choice
    human_input = get_user_input()  # Your function to get user input
    
    # Continue the workflow with human input
    continued_events, final_state = continue_workflow_with_input(state, human_input)
    
    # Access the results from final_state
    print(f"Tech Stack Choice: {final_state.tech_stack_choice}")
    print(f"App Building Prompts: {final_state.app_building_prompts}")
```

## Development

### Adding New Nodes

1. Define the node function in `nodes/workflow_nodes.py`
2. Add the function to the exports in `nodes/__init__.py`
3. Update the graph in `graph.py` to include the new node

### Modifying Prompts

Update the prompt templates in `prompts/templates.py` to change the instructions given to the LLM.

### Extending State

To add new fields to the state:

1. Update the `AgentState` dataclass in `types/agent_state.py`
2. Update the state creation in all node functions

## Requirements

- Python 3.8+
- LangChain
- LangGraph
- OpenAI API key (or compatible LLM provider)

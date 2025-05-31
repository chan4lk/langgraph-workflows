"""Main graph definition for the meta prompter Windsurf workflow."""
from typing import Dict, List, Any, Tuple
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from meta_prompter_windsurf.types import AgentState
from meta_prompter_windsurf.nodes import (
    analyze_requirements,
    generate_ui_flows,
    generate_ui_prompts,
    generate_architecture_prompts,
    human_feedback_tech_stack,
    human_input_required,
    process_tech_stack_choice,
    generate_app_building_prompts,
    generate_ui_automation_prompts
)
from meta_prompter_windsurf.utils import (
    add_human_message_to_state,
    format_results_for_output,
    router
)
from langchain_core.messages import HumanMessage

# Initialize the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze_requirements", analyze_requirements)
workflow.add_node("generate_ui_flows", generate_ui_flows)
workflow.add_node("generate_ui_prompts", generate_ui_prompts)
workflow.add_node("generate_architecture_prompts", generate_architecture_prompts)
workflow.add_node("human_feedback_tech_stack", human_feedback_tech_stack)
workflow.add_node("human_input_required", human_input_required)
workflow.add_node("process_tech_stack_choice", process_tech_stack_choice)
workflow.add_node("generate_app_building_prompts", generate_app_building_prompts)
workflow.add_node("generate_ui_automation_prompts", generate_ui_automation_prompts)

# Add conditional edges with the router
workflow.add_conditional_edges(
    "human_input_required",
    router,
    {
        "human_input_required": "human_input_required",  # Loop back to wait for input
        "process_tech_stack_choice": "process_tech_stack_choice",
        "generate_app_building_prompts": "generate_app_building_prompts"
    }
)

# Add regular edges
workflow.add_edge("analyze_requirements", "generate_ui_flows")
workflow.add_edge("generate_ui_flows", "generate_ui_prompts")
workflow.add_edge("generate_ui_prompts", "generate_architecture_prompts")
workflow.add_edge("generate_architecture_prompts", "human_feedback_tech_stack")
workflow.add_edge("human_feedback_tech_stack", "human_input_required")
workflow.add_edge("process_tech_stack_choice", "generate_app_building_prompts")
workflow.add_edge("generate_app_building_prompts", "generate_ui_automation_prompts")
workflow.add_edge("generate_ui_automation_prompts", END)

# Set entry point
workflow.set_entry_point("analyze_requirements")

# Export the compiled graph
graph = workflow.compile()


# Function to run the workflow
def run_meta_prompter(app_idea: str) -> Dict:
    """
    Run the meta prompter workflow with an app idea
    
    Args:
        app_idea (str): Description of the app idea
        
    Returns:
        Dict: Contains the analyzed requirements, UI flows, UI prompts, architecture prompts,
              app building prompts, and UI automation prompts
    """
    # Initialize state
    initial_state = AgentState(
        messages=[HumanMessage(content=app_idea)]
    )
    
    # Run the workflow
    result = graph.invoke(initial_state)
    
    # Return the results
    return format_results_for_output(result)


def run_meta_prompter_interactive(app_idea: str):
    """
    Run the meta prompter workflow interactively, allowing for human input
    
    Args:
        app_idea (str): Description of the app idea
        
    Returns:
        Tuple containing:
        - List of events from the workflow execution
        - Final state of the workflow
        - Boolean indicating if human input is required
    """
    # Initialize state
    initial_state = AgentState(
        messages=[HumanMessage(content=app_idea)]
    )
    
    # Create a config to stream the workflow
    config = {"recursion_limit": 25}
    
    # Stream the workflow
    events = []
    current_state = initial_state
    
    for event in graph.stream(initial_state, config):
        events.append(event)
        
        # Update the current state if available in the event
        if "value" in event and isinstance(event["value"], AgentState):
            current_state = event["value"]
        
        # Check if we've reached the human input node
        if current_state.current_step == "human_input_required":
            # Return the current events, state, and a flag indicating human input is needed
            return events, current_state, True
    
    # If we've completed the workflow without needing human input
    return events, current_state, False


def continue_workflow_with_input(state: AgentState, human_input: str):
    """
    Continue the workflow from a paused state with human input
    
    Args:
        state (AgentState): Current state of the workflow
        human_input (str): Human input to add to the workflow
        
    Returns:
        Tuple containing:
        - List of events from the continued workflow execution
        - Final state of the workflow
    """
    # Add the human input to the state
    new_state = add_human_message_to_state(state, human_input)
    
    # Create a config to stream the workflow
    config = {"recursion_limit": 25}
    
    # Continue the workflow
    events = []
    current_state = new_state
    
    for event in graph.stream(new_state, config):
        events.append(event)
        
        # Update the current state if available in the event
        if "value" in event and isinstance(event["value"], AgentState):
            current_state = event["value"]
    
    # Return the events and final state
    return events, current_state

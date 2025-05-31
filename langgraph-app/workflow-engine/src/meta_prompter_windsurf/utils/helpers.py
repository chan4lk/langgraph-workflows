"""
Helper functions for the meta prompter Windsurf workflow.
"""
from typing import List, Dict, Any, Union
from langchain_core.messages import HumanMessage
from meta_prompter_windsurf.types import AgentState


def add_human_message_to_state(state: AgentState, message: str) -> AgentState:
    """
    Add a human message to the state and return the updated state
    
    Args:
        state (AgentState): Current state of the workflow
        message (str): Human message to add
        
    Returns:
        AgentState: Updated state with the human message
    """
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=state.ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step=state.current_step
    )
    
    # Add the human message
    new_state.messages.append(HumanMessage(content=message))
    
    return new_state


def format_results_for_output(state: Any) -> Dict:
    """
    Format the state results for output
    
    Args:
        state: Final state of the workflow (could be AgentState or a dict-like object)
        
    Returns:
        Dict: Contains the analyzed requirements, UI flows, UI prompts, architecture prompts,
              app building prompts, and UI automation prompts
    """
    # Handle different state formats
    if hasattr(state, "value") and hasattr(state.value, "app_requirements"):
        # New LangGraph format where state is wrapped
        state_obj = state.value
    elif hasattr(state, "app_requirements"):
        # Direct AgentState object
        state_obj = state
    else:
        # Dictionary-like object
        return {
            "requirements": state.get("app_requirements", {}),
            "ui_flows": state.get("ui_flows", []),
            "ui_prompts": state.get("ui_prompts", []),
            "architecture_prompts": state.get("architecture_prompts", []),
            "tech_stack_choice": state.get("tech_stack_choice", None),
            "app_building_prompts": state.get("app_building_prompts", []),
            "ui_automation_prompts": state.get("ui_automation_prompts", [])
        }
    
    # Return formatted output from state object
    return {
        "requirements": state_obj.app_requirements,
        "ui_flows": state_obj.ui_flows,
        "ui_prompts": state_obj.ui_prompts,
        "architecture_prompts": state_obj.architecture_prompts,
        "tech_stack_choice": state_obj.tech_stack_choice,
        "app_building_prompts": state_obj.app_building_prompts,
        "ui_automation_prompts": state_obj.ui_automation_prompts
    }


def router(state: AgentState) -> str:
    """
    Route to the appropriate node based on the current step.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        str: Name of the next node to execute
    """
    if state.current_step == "human_input_required":
        # Check if we have a new human message
        if state.messages and isinstance(state.messages[-1], HumanMessage):
            # Check if this human message has been processed before
            # We'll use a simple heuristic: if tech_stack_choice is already set, we've processed it
            if state.tech_stack_choice is None:
                return "process_tech_stack_choice"
            else:
                # If we've already processed this message, continue to the next step
                return "generate_app_building_prompts"
        else:
            # If no human message yet, use process_tech_stack_choice with a default value
            # to avoid infinite loops
            return "process_tech_stack_choice"
    else:
        # For all other steps, use the current_step value
        return state.current_step

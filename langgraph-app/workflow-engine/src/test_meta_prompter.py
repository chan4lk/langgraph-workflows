"""
Test script for the meta prompter Windsurf workflow.
"""
import os
import json
from typing import Dict, Any
from meta_prompter_windsurf import (
    run_meta_prompter,
    run_meta_prompter_interactive,
    continue_workflow_with_input
)
import dotenv

dotenv.load_dotenv()

def test_non_interactive_workflow():
    """Test the non-interactive workflow."""
    # Simple app idea for testing
    app_idea = "A task management app that helps users organize their daily tasks, set priorities, and track progress."
    
    # Run the workflow
    print("Running non-interactive workflow...")
    result = run_meta_prompter(app_idea)
    
    # Print the results
    print("\nWorkflow completed!")
    print(f"Requirements: {len(result['requirements'])} items")
    print(f"UI Flows: {len(result['ui_flows'])} screens")
    print(f"UI Prompts: {len(result['ui_prompts'])} prompts")
    print(f"Architecture Prompts: {len(result['architecture_prompts'])} components")
    print(f"Tech Stack Choice: {result['tech_stack_choice']}")
    print(f"App Building Prompts: {len(result['app_building_prompts'])} components")
    print(f"UI Automation Prompts: {len(result['ui_automation_prompts'])} tests")
    
    return result


def test_interactive_workflow():
    """Test the interactive workflow with human input."""
    # Simple app idea for testing
    app_idea = "A recipe sharing platform where users can upload, search, and rate recipes."
    
    # Run the workflow until human input is required
    print("Running interactive workflow...")
    events, state, human_input_required = run_meta_prompter_interactive(app_idea)
    
    if human_input_required:
        print("\nHuman input required!")
        print(f"Current step: {state.current_step}")
        
        # Get the last AI message which should contain tech stack options
        last_ai_message = None
        for msg in reversed(state.messages):
            if hasattr(msg, "type") and msg.type == "ai":
                last_ai_message = msg.content
            elif isinstance(msg, dict) and msg.get("role") == "assistant":
                last_ai_message = msg.get("content", "")
            if last_ai_message:
                break
        
        if last_ai_message:
            print(f"\nAI Message: {last_ai_message[:200]}...\n")
        
        # Simulate human input
        human_input = "I choose the MERN stack (MongoDB, Express.js, React, Node.js)"
        print(f"Human input: {human_input}")
        
        # Continue the workflow with human input
        print("\nContinuing workflow with human input...")
        continued_events, final_state = continue_workflow_with_input(state, human_input)
        
        # Print the results
        print("\nWorkflow completed!")
        print(f"Tech Stack Choice: {final_state.tech_stack_choice}")
        print(f"App Building Prompts: {len(final_state.app_building_prompts)} components")
        print(f"UI Automation Prompts: {len(final_state.ui_automation_prompts)} tests")
        
        return final_state
    else:
        print("\nWorkflow completed without requiring human input!")
        return state


if __name__ == "__main__":
    # Set your OpenAI API key
    # Uncomment the test you want to run
    test_non_interactive_workflow()
    # test_interactive_workflow()
    
    print("\nTo run the tests, uncomment one of the test functions in the main block.")
    print("Make sure to set your OpenAI API key in the environment variable.")

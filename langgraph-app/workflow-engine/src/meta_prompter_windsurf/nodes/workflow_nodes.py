"""
Node functions for the meta prompter Windsurf workflow.
"""
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.schema.runnable import RunnablePassthrough

from meta_prompter_windsurf.types import AgentState
from meta_prompter_windsurf.prompts.templates import (
    requirements_prompt,
    ui_flow_prompt,
    ui_prompt_template,
    architecture_prompt,
    tech_stack_prompt,
    app_building_prompt,
    ui_automation_prompt
)
from meta_prompter_windsurf.parsers.output_parsers import (
    requirements_parser,
    ui_flow_parser,
    ui_prompt_parser,
    architecture_prompt_parser,
    app_building_prompt_parser,
    ui_automation_prompt_parser
)


def analyze_requirements(state: AgentState) -> AgentState:
    """
    Analyze the app idea and extract requirements.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with requirements
    """
    from meta_prompter_windsurf.utils import normalize_messages, extract_last_message_content
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = requirements_prompt | llm | requirements_parser
    
    # Normalize messages and extract the last message content
    normalized_messages = normalize_messages(state.messages)
    input_text = extract_last_message_content(normalized_messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "input": input_text
    })
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=result,
        ui_flows=state.ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step="generate_ui_flows"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=str(result)))
    
    return new_state


def generate_ui_flows(state: AgentState) -> AgentState:
    """
    Generate UI flows based on requirements.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with UI flows
    """
    from meta_prompter_windsurf.utils import normalize_messages
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = ui_flow_prompt | llm
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "requirements": state.app_requirements
    })
    
    # Parse the result
    ui_flows = ui_flow_parser(result.content)
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step="generate_ui_prompts"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=result.content))
    
    return new_state


def generate_ui_prompts(state: AgentState) -> AgentState:
    """
    Generate UI prompts based on UI flows.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with UI prompts
    """
    from meta_prompter_windsurf.utils import normalize_messages
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = ui_prompt_template | llm
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "ui_flows": state.ui_flows
    })
    
    # Parse the result
    ui_prompts = ui_prompt_parser(result.content)
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=state.ui_flows,
        ui_prompts=ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step="generate_architecture_prompts"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=result.content))
    
    return new_state


def generate_architecture_prompts(state: AgentState) -> AgentState:
    """
    Generate architecture prompts based on requirements and UI flows.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with architecture prompts
    """
    from meta_prompter_windsurf.utils import normalize_messages
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = architecture_prompt | llm
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "requirements": state.app_requirements,
        "ui_flows": state.ui_flows
    })
    
    # Parse the result
    architecture_prompts = architecture_prompt_parser(result.content)
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=state.ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step="human_feedback_tech_stack"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=result.content))
    
    return new_state


def human_feedback_tech_stack(state: AgentState) -> AgentState:
    """
    Get human feedback for tech stack choice.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with tech stack recommendations
    """
    from meta_prompter_windsurf.utils import normalize_messages
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = tech_stack_prompt | llm
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "requirements": state.app_requirements,
        "architecture_prompts": state.architecture_prompts
    })
    
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
        current_step="human_input_required"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=result.content))
    
    return new_state


def human_input_required(state: AgentState) -> AgentState:
    """
    This node handles the state when human input is required.
    It adds a message to the state indicating that input is needed.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with human input prompt
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
        current_step="human_input_required"
    )
    
    return new_state


def process_tech_stack_choice(state: AgentState) -> AgentState:
    """
    Process the tech stack choice from human input.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with tech stack choice
    """
    from meta_prompter_windsurf.utils import normalize_messages, extract_last_message_content
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Get the tech stack choice from the last human message if available
    tech_stack_choice = None
    if normalized_messages and isinstance(normalized_messages[-1], HumanMessage):
        tech_stack_choice = extract_last_message_content(normalized_messages)
    
    # If no human message or empty content, use a default
    if not tech_stack_choice:
        tech_stack_choice = "Default MERN Stack (MongoDB, Express.js, React, Node.js)"
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=state.ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step="generate_app_building_prompts"
    )
    
    return new_state


def generate_app_building_prompts(state: AgentState) -> AgentState:
    """
    Generate app building prompts based on requirements, UI flows, architecture, and tech stack.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with app building prompts
    """
    from meta_prompter_windsurf.utils import normalize_messages
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = app_building_prompt | llm
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "requirements": state.app_requirements,
        "ui_flows": state.ui_flows,
        "architecture_prompts": state.architecture_prompts,
        "tech_stack": state.tech_stack_choice
    })
    
    # Parse the result
    app_building_prompts = app_building_prompt_parser(result.content)
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=state.ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=app_building_prompts,
        ui_automation_prompts=state.ui_automation_prompts,
        current_step="generate_ui_automation_prompts"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=result.content))
    
    return new_state


def generate_ui_automation_prompts(state: AgentState) -> AgentState:
    """
    Generate UI automation prompts based on UI flows and app building prompts.
    
    Args:
        state (AgentState): Current state of the workflow
        
    Returns:
        AgentState: Updated state with UI automation prompts
    """
    from meta_prompter_windsurf.utils import normalize_messages
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = ui_automation_prompt | llm
    
    # Normalize messages
    normalized_messages = normalize_messages(state.messages)
    
    # Run the chain
    result = chain.invoke({
        "messages": normalized_messages,
        "requirements": state.app_requirements,
        "ui_flows": state.ui_flows,
        "app_building_prompts": state.app_building_prompts
    })
    
    # Parse the result
    ui_automation_prompts = ui_automation_prompt_parser(result.content)
    
    # Create a copy of the state
    new_state = AgentState(
        messages=list(state.messages),
        app_requirements=state.app_requirements,
        ui_flows=state.ui_flows,
        ui_prompts=state.ui_prompts,
        architecture_prompts=state.architecture_prompts,
        tech_stack_choice=state.tech_stack_choice,
        app_building_prompts=state.app_building_prompts,
        ui_automation_prompts=ui_automation_prompts,
        current_step="END"
    )
    
    # Add the AI message
    new_state.messages.append(AIMessage(content=result.content))
    
    return new_state

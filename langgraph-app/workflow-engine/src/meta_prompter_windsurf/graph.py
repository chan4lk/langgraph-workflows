from typing import Dict, List, Tuple, Any, Sequence, Optional
from typing_extensions import Annotated
from dataclasses import field, dataclass
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, add_messages
import json

# Define the state type
@dataclass
class AgentState:
    """State for the meta prompter agent."""
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)
    app_requirements: Dict = field(default_factory=dict)
    ui_flows: List[Dict] = field(default_factory=list)
    ui_prompts: List[str] = field(default_factory=list)
    architecture_prompts: List[Dict] = field(default_factory=list)
    tech_stack_choice: Optional[str] = field(default=None)
    app_building_prompts: List[Dict] = field(default_factory=list)
    ui_automation_prompts: List[Dict] = field(default_factory=list)
    current_step: str = field(default="analyze_requirements")

    def __repr__(self) -> str:
        return f"AgentState(messages={self.messages}, current_step={self.current_step})"

# Requirements Analysis Agent
requirements_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert requirements analyst. Your task is to analyze app ideas and break them down into detailed requirements.
    Consider the following aspects:
    1. Core Features
    2. User Types/Roles
    3. Data Models
    4. Business Rules
    5. Technical Requirements
    6. Security Requirements
    
    Output should be in JSON format with these categories."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])

requirements_parser = JsonOutputParser()

def analyze_requirements(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = requirements_prompt | llm | requirements_parser
    
    # Get the last message if it exists
    input_text = state.messages[-1].content if state.messages else ""
    
    # Run the chain
    result = chain.invoke({
        "messages": state.messages,
        "input": input_text
    })
    
    # Add AI message to state
    state.messages.append(
        AIMessage(content=json.dumps(result, indent=2))
    )
    
    # Update state
    state.app_requirements = result
    state.current_step = "generate_ui_flows"
    return state

# UI Flow Generator Agent
ui_flow_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a UI/UX expert. Based on the provided app requirements, generate a detailed screen flow.
    For each screen, specify:
    1. Screen Name
    2. Purpose
    3. Key Components
    4. User Interactions
    5. Navigation Flows
    6. Data Display/Input Requirements
    
    Output should be in JSON format with an array of screens."""),
    ("human", "Requirements: {requirements}"),
])

ui_flow_parser = JsonOutputParser()

def generate_ui_flows(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = ui_flow_prompt | llm | ui_flow_parser
    
    # Run the chain
    result = chain.invoke({
        "requirements": json.dumps(state.app_requirements, indent=2)
    })
    
    # Add AI message to state
    state.messages.append(
        AIMessage(content=json.dumps(result, indent=2))
    )
    
    # Update state
    state.ui_flows = result
    state.current_step = "generate_ui_prompts"
    return state

# UI Prompt Generator Agent
ui_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a UI/UX expert specializing in creating detailed screen descriptions.
    For the given screen details, generate a detailed prompt following this exact format:
    
    Product Description: [Screen Name]
    
    [Brief description of the screen's purpose and main functionality in 2-3 sentences]
    
    Structure and Layout: [Describe how the interface is divided into sections]
    
    Components:
    [Numbered list of components with their specific locations and purposes]
    
    [One sentence concluding statement about the screen's value proposition]
    
    Example format:
    Product Description: BlogEase - Post Creation & Publishing Screen
    
    BlogEase streamlines your blogging process with its intuitive desktop web application interface for creating and publishing posts.
    
    Structure and Layout: The interface is organized into four key sections.
    
    Components:
    1. Title Bar: Situated at the top with input fields for post title and categories
    2. Content Editor: Centrally located, featuring a rich text editor for drafting and formatting content
    3. Sidebar: On the left, containing tools for tags, SEO settings, and featured image selection
    4. Action Panel: At the bottom, offering preview, save, and publish buttons with scheduling options
    
    BlogEase empowers bloggers with a seamless post management experience."""),
    ("human", """Generate a prompt for this screen:
    {screen_details}"""),
])

def generate_ui_prompts(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = ui_prompt_template | llm
    
    # Generate prompts for each screen
    prompts = []
    for screen in state.ui_flows:
        # Convert screen details to a more readable format
        screen_details = json.dumps(screen, indent=2)
        
        # Generate prompt for this screen
        result = chain.invoke({
            "screen_details": screen_details
        })
        
        # Add the generated prompt
        prompts.append(result.content)
        
        # Add AI message to state with screen name if available
        screen_name = screen["Screen Name"] if isinstance(screen, dict) and "Screen Name" in screen else "Unknown Screen"
        state.messages.append(
            AIMessage(content=f"Generated prompt for screen '{screen_name}':\n\n{result.content}")
        )
    
    # Update state
    state.ui_prompts = prompts
    state.current_step = END
    return state

def should_continue(state: AgentState) -> str:
    """Determine the next node in the graph."""
    return state.current_step

# Architecture Prompt Generator Agent
architecture_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior software architect specializing in creating scalable, maintainable, and secure applications.
    Based on the UI requirements and flows, generate detailed prompts for defining the application architecture.
    
    Focus on these key aspects:
    1. Scalability - How the architecture will handle growth in users and data
    2. Security - Authentication, authorization, data protection, and secure coding practices
    3. Testability - How the code can be effectively tested (unit, integration, e2e)
    4. Maintainability - Code organization, modularization, and documentation
    
    For each aspect, create specific Windsurf prompts that will help generate:
    - Architecture diagrams
    - Component structure
    - Data flow diagrams
    - Rule files for code generation
    - Markdown documentation for domain understanding
    
    Your output should be in JSON format with the following structure:
    {{
      "architecture_prompts": [
        {{
          "title": "Title of the prompt",
          "description": "Detailed description of what this prompt will generate",
          "prompt_text": "The actual prompt text to be used with Windsurf",
          "expected_output": "Description of what output this prompt will produce",
          "category": "One of: diagram, structure, rules, documentation"
        }}
      ]
    }}"""),
    ("human", """Generate architecture prompts based on these requirements and UI flows:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    UI Prompts: {ui_prompts}""")
])

architecture_parser = JsonOutputParser()

def generate_architecture_prompts(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = architecture_prompt | llm | architecture_parser
    
    # Run the chain
    result = chain.invoke({
        "requirements": json.dumps(state.app_requirements, indent=2),
        "ui_flows": json.dumps(state.ui_flows, indent=2),
        "ui_prompts": "\n\n".join(state.ui_prompts)
    })
    
    # Add AI message to state
    state.messages.append(
        AIMessage(content=f"Generated {len(result['architecture_prompts'])} architecture prompts")
    )
    
    # Update state
    state.architecture_prompts = result["architecture_prompts"]
    state.current_step = "human_feedback_tech_stack"
    return state

# Human Feedback for Tech Stack Choice
tech_stack_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a technical advisor helping to choose the best tech stack for an application.
    Based on the requirements and architecture, provide a clear recommendation for tech stack options.
    
    Present the options in a clear, concise manner that helps the user make an informed decision.
    Focus on NextJS or Vite (React) with Python backend options as preferred by the user.
    
    For each option, explain:
    1. Benefits for this specific application
    2. Potential challenges
    3. How it aligns with the architectural requirements
    
    Format your response as a clear question asking which tech stack the user prefers."""),
    ("human", """Based on these requirements and architecture prompts, recommend tech stack options:
    
    Requirements: {requirements}
    
    Architecture Prompts: {architecture_prompts}""")
])

def human_feedback_tech_stack(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = tech_stack_prompt | llm
    
    # Run the chain
    result = chain.invoke({
        "requirements": json.dumps(state.app_requirements, indent=2),
        "architecture_prompts": json.dumps(state.architecture_prompts, indent=2)
    })
    
    # Add AI message to state
    state.messages.append(
        AIMessage(content=result.content)
    )
    
    # Set current step to wait for human input
    state.current_step = "human_input_required"
    return state

def process_tech_stack_choice(state: AgentState) -> AgentState:
    # Get the last human message as the tech stack choice
    if state.messages and isinstance(state.messages[-1], HumanMessage):
        state.tech_stack_choice = state.messages[-1].content
        
        # Add confirmation message
        state.messages.append(
            AIMessage(content=f"Tech stack choice recorded: {state.tech_stack_choice}")
        )
    else:
        # If no human message, use a default tech stack
        default_tech_stack = "NextJS with Python backend"
        state.tech_stack_choice = default_tech_stack
        
        # Add message about using default
        state.messages.append(
            AIMessage(content=f"No tech stack choice provided. Using default: {default_tech_stack}")
        )
    
    state.current_step = "generate_app_building_prompts"
    return state

# App Building Prompt Generator
app_building_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert in application development using Windsurf code generation.
    Based on the requirements, UI flows, architecture, and selected tech stack, generate a maximum of 10 Windsurf prompts
    that will build the complete application.
    
    Each prompt should:
    1. Focus on a specific part of the application
    2. Be clear and detailed enough for Windsurf to generate high-quality code
    3. Include necessary context about dependencies and relationships
    4. Specify expected outputs and file structure
    
    Your output should be in JSON format with the following structure:
    {{
      "app_building_prompts": [
        {{
          "title": "Title of the prompt",
          "description": "Detailed description of what this prompt will generate",
          "prompt_text": "The actual prompt text to be used with Windsurf",
          "expected_output": "Description of what output this prompt will produce",
          "order": "Numerical order in which this prompt should be executed (1-10)"
        }}
      ]
    }}"""),
    ("human", """Generate app building prompts based on:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    Architecture Prompts: {architecture_prompts}
    
    Selected Tech Stack: {tech_stack}""")
])

app_building_parser = JsonOutputParser()

def generate_app_building_prompts(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = app_building_prompt | llm | app_building_parser
    
    # Run the chain
    result = chain.invoke({
        "requirements": json.dumps(state.app_requirements, indent=2),
        "ui_flows": json.dumps(state.ui_flows, indent=2),
        "architecture_prompts": json.dumps(state.architecture_prompts, indent=2),
        "tech_stack": state.tech_stack_choice
    })
    
    # Add AI message to state
    state.messages.append(
        AIMessage(content=f"Generated {len(result['app_building_prompts'])} app building prompts")
    )
    
    # Update state
    state.app_building_prompts = result["app_building_prompts"]
    state.current_step = "generate_ui_automation_prompts"
    return state

# UI Automation Prompt Generator
ui_automation_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a QA automation expert specializing in Playwright for UI testing.
    Based on the application requirements and UI flows, generate prompts for creating comprehensive UI automation tests.
    
    Your prompts should cover:
    1. Setup and configuration of Playwright
    2. Test structure and organization
    3. Page object models
    4. Test scenarios for critical user journeys
    5. Test data management
    6. Reporting and CI/CD integration
    
    Your output should be in JSON format with the following structure:
    {{
      "ui_automation_prompts": [
        {{
          "title": "Title of the prompt",
          "description": "Detailed description of what this prompt will generate",
          "prompt_text": "The actual prompt text to be used with Windsurf",
          "expected_output": "Description of what output this prompt will produce",
          "test_coverage": "Description of what functionality this test will cover"
        }}
      ]
    }}"""),
    ("human", """Generate UI automation prompts based on:
    
    Requirements: {requirements}
    
    UI Flows: {ui_flows}
    
    Tech Stack: {tech_stack}""")
])

ui_automation_parser = JsonOutputParser()

def generate_ui_automation_prompts(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = ui_automation_prompt | llm | ui_automation_parser
    
    # Run the chain
    result = chain.invoke({
        "requirements": json.dumps(state.app_requirements, indent=2),
        "ui_flows": json.dumps(state.ui_flows, indent=2),
        "tech_stack": state.tech_stack_choice
    })
    
    # Add AI message to state
    state.messages.append(
        AIMessage(content=f"Generated {len(result['ui_automation_prompts'])} UI automation prompts")
    )
    
    # Update state
    state.ui_automation_prompts = result["ui_automation_prompts"]
    state.current_step = END
    return state

# Define a node for human input required
def human_input_required(state: AgentState) -> AgentState:
    """
    This node handles the state when human input is required.
    It adds a message to the state indicating that input is needed.
    """
    # Check if we've already added a message asking for input
    if not state.messages or not isinstance(state.messages[-1], AIMessage) or not state.messages[-1].content.startswith("Please select a tech stack"):
        # Add a message asking for input
        state.messages.append(
            AIMessage(content="Please select a tech stack for your application. Options include: NextJS, Vite+React, Angular, Vue, or others. What would you prefer?")
        )
    
    # Keep the current step as human_input_required
    # The router will handle moving to the next step when input is received
    return state

# Define a router function for handling human input
def router(state: AgentState) -> str:
    """Route to the appropriate node based on the current step."""
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
            # If no human message yet, we need to wait
            # In an interactive context, this would pause execution until human input is received
            # For non-interactive runs, we'll use process_tech_stack_choice with a default value
            # to avoid infinite loops
            return "process_tech_stack_choice"
    else:
        # For all other steps, use the current_step value
        return state.current_step

# Initialize the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze_requirements", analyze_requirements)
workflow.add_node("generate_ui_flows", generate_ui_flows)
workflow.add_node("generate_ui_prompts", generate_ui_prompts)
workflow.add_node("generate_architecture_prompts", generate_architecture_prompts)
workflow.add_node("human_feedback_tech_stack", human_feedback_tech_stack)
workflow.add_node("human_input_required", human_input_required)  # Use the proper function
workflow.add_node("process_tech_stack_choice", process_tech_stack_choice)
workflow.add_node("generate_app_building_prompts", generate_app_building_prompts)
workflow.add_node("generate_ui_automation_prompts", generate_ui_automation_prompts)

# Add conditional edges with the router
workflow.add_conditional_edges(
    "human_input_required",
    router,
    {
        "human_input_required": "human_input_required",  # Loop back to wait for input
        "process_tech_stack_choice": "process_tech_stack_choice"
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
    return {
        "requirements": result.app_requirements,
        "ui_flows": result.ui_flows,
        "ui_prompts": result.ui_prompts,
        "architecture_prompts": result.architecture_prompts,
        "tech_stack_choice": result.tech_stack_choice,
        "app_building_prompts": result.app_building_prompts,
        "ui_automation_prompts": result.ui_automation_prompts
    }

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
    for event in graph.stream(initial_state, config):
        events.append(event)
        
        # Check if we've reached the human input node
        if event.get("state") and event["state"].current_step == "human_input_required":
            # Return the current events, state, and a flag indicating human input is needed
            return events, event["state"], True
    
    # If we've completed the workflow without needing human input
    final_state = events[-1]["state"] if events else initial_state
    return events, final_state, False

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
    for event in graph.stream(new_state, config):
        events.append(event)
    
    # Return the events and final state
    final_state = events[-1]["state"] if events else new_state
    return events, final_state

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

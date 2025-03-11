from typing import Dict, List, Tuple, Any, Sequence
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
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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

# Initialize the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze_requirements", analyze_requirements)
workflow.add_node("generate_ui_flows", generate_ui_flows)
workflow.add_node("generate_ui_prompts", generate_ui_prompts)

# Add edges
workflow.add_edge("analyze_requirements", "generate_ui_flows")
workflow.add_edge("generate_ui_flows", "generate_ui_prompts")
workflow.add_edge("generate_ui_prompts", END)

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
        Dict: Contains the analyzed requirements, UI flows, and UI prompts
    """
    # Initialize state
    initial_state = AgentState(
        messages=[HumanMessage(content=app_idea)]
    )
    
    # Run the workflow
    result = graph.invoke(initial_state)
    
    return {
        "requirements": result.app_requirements,
        "ui_flows": result.ui_flows,
        "ui_prompts": result.ui_prompts
    }

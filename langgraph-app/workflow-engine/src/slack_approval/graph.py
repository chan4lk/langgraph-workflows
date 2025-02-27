"""Define a workflow for processing leads from Slack.

This workflow handles the entire process from lead extraction to Hubspot creation and notification.
"""

from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional, Any, TypedDict, cast

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from slack_approval.configuration import Configuration
from slack_approval.tools import tools
from slack_approval.state import State, InputState, LeadAttributes
from slack_approval.utils import load_chat_model, extract_slack_message, create_initial_message


# Define node functions

async def extract_lead_info(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Extract lead information from the Slack message.
    
    Args:
        state: The current state
        config: Configuration for the node
        
    Returns:
        Updated state with extracted lead information
    """
    if not state.slack_event:
        return {
            "messages": [
                AIMessage(content="No Slack event found. Cannot process lead.")
            ]
        }
    
    # Create a message to extract lead information
    slack_message = extract_slack_message(state.slack_event)
    
    # Use the extract_lead_attributes tool
    model = load_chat_model("openai/gpt-4o-mini").bind_tools([tools[0]])  # extract_lead_attributes tool
    
    # Prepare the prompt
    prompt = f"""
    Please extract the key attributes from this Slack message:
    
    {slack_message}
    
    Extract the geo_location, industry, and engagement information.
    """
    
    # Call the model
    response = await model.ainvoke(
        [HumanMessage(content=prompt)],
        config
    )
    
    # Extract the tool calls
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        lead_attributes = tool_call.get("output", {})
        
        # Update the state
        return {
            "lead_attributes": LeadAttributes(
                geo_location=lead_attributes.get("geo_location"),
                industry=lead_attributes.get("industry"),
                engagement=lead_attributes.get("engagement")
            ),
            "messages": [
                AIMessage(content=f"Extracted lead attributes: {lead_attributes}")
            ]
        }
    
    return {
        "messages": [
            AIMessage(content="Failed to extract lead attributes.")
        ]
    }


async def assign_sales_person_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Assign a sales person based on the lead attributes.
    
    Args:
        state: The current state
        config: Configuration for the node
        
    Returns:
        Updated state with assigned sales person
    """
    if not state.lead_attributes:
        return {
            "messages": [
                AIMessage(content="No lead attributes found. Cannot assign sales person.")
            ]
        }
    
    # Use the assign_sales_person tool
    model = load_chat_model("openai/gpt-4o-mini").bind_tools([tools[1]])  # assign_sales_person tool
    
    # Prepare the prompt
    attributes = state.lead_attributes.to_dict()
    prompt = f"""
    Please assign a sales person based on these lead attributes:
    
    Geo Location: {attributes.get('geo_location')}
    Industry: {attributes.get('industry')}
    Engagement: {attributes.get('engagement')}
    
    Use the assignment criteria to determine the appropriate sales person.
    """
    
    # Call the model
    response = await model.ainvoke(
        [HumanMessage(content=prompt)],
        config
    )
    
    # Extract the tool calls
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        assigned_person = tool_call.get("output", "Sales Team")
        
        # Update the state
        return {
            "assigned_sales_person": assigned_person,
            "messages": [
                AIMessage(content=f"Assigned sales person: {assigned_person}")
            ]
        }
    
    return {
        "messages": [
            AIMessage(content="Failed to assign sales person.")
        ]
    }


async def send_approval_request_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Send an approval request to the admin.
    
    Args:
        state: The current state
        config: Configuration for the node
        
    Returns:
        Updated state with approval status
    """
    if not state.lead_attributes or not state.assigned_sales_person:
        return {
            "messages": [
                AIMessage(content="Missing lead attributes or assigned sales person. Cannot send approval request.")
            ]
        }
    
    # Use the send_approval_request tool
    model = load_chat_model("openai/gpt-4o-mini").bind_tools([tools[2]])  # send_approval_request tool
    
    # Prepare the prompt
    attributes = state.lead_attributes.to_dict()
    prompt = f"""
    Please send an approval request for this lead assignment:
    
    Lead Attributes:
    - Geo Location: {attributes.get('geo_location')}
    - Industry: {attributes.get('industry')}
    - Engagement: {attributes.get('engagement')}
    
    Assigned Sales Person: {state.assigned_sales_person}
    
    Send an approval request to the admin.
    """
    
    # Call the model
    response = await model.ainvoke(
        [HumanMessage(content=prompt)],
        config
    )
    
    # Extract the tool calls
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        approval_sent = tool_call.get("output", False)
        
        # Update the state
        return {
            "approval_status": approval_sent,
            "messages": [
                AIMessage(content=f"Approval request sent: {approval_sent}")
            ]
        }
    
    return {
        "messages": [
            AIMessage(content="Failed to send approval request.")
        ]
    }


async def create_hubspot_lead_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Create a lead in Hubspot.
    
    Args:
        state: The current state
        config: Configuration for the node
        
    Returns:
        Updated state with Hubspot lead creation status
    """
    if not state.lead_attributes or not state.assigned_sales_person or not state.approval_status:
        return {
            "messages": [
                AIMessage(content="Missing required information or approval not granted. Cannot create Hubspot lead.")
            ]
        }
    
    # Use the create_hubspot_lead tool
    model = load_chat_model("openai/gpt-4o-mini").bind_tools([tools[3]])  # create_hubspot_lead tool
    
    # Prepare the prompt
    attributes = state.lead_attributes.to_dict()
    prompt = f"""
    Please create a lead in Hubspot with the following information:
    
    Lead Attributes:
    - Geo Location: {attributes.get('geo_location')}
    - Industry: {attributes.get('industry')}
    - Engagement: {attributes.get('engagement')}
    
    Assigned Sales Person: {state.assigned_sales_person}
    """
    
    # Call the model
    response = await model.ainvoke(
        [HumanMessage(content=prompt)],
        config
    )
    
    # Extract the tool calls
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        lead_created = tool_call.get("output", False)
        
        # Update the state
        return {
            "hubspot_lead_created": lead_created,
            "messages": [
                AIMessage(content=f"Hubspot lead created: {lead_created}")
            ]
        }
    
    return {
        "messages": [
            AIMessage(content="Failed to create Hubspot lead.")
        ]
    }


async def notify_sales_person_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Notify the assigned sales person.
    
    Args:
        state: The current state
        config: Configuration for the node
        
    Returns:
        Updated state with notification status
    """
    if not state.assigned_sales_person or not state.hubspot_lead_created:
        return {
            "messages": [
                AIMessage(content="Missing assigned sales person or Hubspot lead not created. Cannot send notification.")
            ]
        }
    
    # Use the notify_sales_person tool
    model = load_chat_model("openai/gpt-4o-mini").bind_tools([tools[4]])  # notify_sales_person tool
    
    # Prepare the prompt
    prompt = f"""
    Please notify the assigned sales person about the new lead:
    
    Sales Person: {state.assigned_sales_person}
    
    Send a notification to inform them about the new lead assignment.
    """
    
    # Call the model
    response = await model.ainvoke(
        [HumanMessage(content=prompt)],
        config
    )
    
    # Extract the tool calls
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        notification_sent = tool_call.get("output", False)
        
        # Update the state
        return {
            "notification_sent": notification_sent,
            "messages": [
                AIMessage(content=f"Notification sent to {state.assigned_sales_person}: {notification_sent}")
            ]
        }
    
    return {
        "messages": [
            AIMessage(content="Failed to send notification.")
        ]
    }


async def process_slack_event(state: InputState) -> State:
    """Process the incoming Slack event and initialize the workflow state.
    
    Args:
        state: The input state with the Slack event
        
    Returns:
        Initialized workflow state
    """
    # Create the initial state
    workflow_state = State(
        messages=list(state.messages),
        slack_event=state.slack_event,
        is_last_step=False,
        lead_attributes=None,
        assigned_sales_person=None,
        approval_status=None,
        hubspot_lead_created=False,
        notification_sent=False
    )
    
    # Add an initial message if the slack event exists
    if state.slack_event:
        initial_message = create_initial_message(state.slack_event)
        workflow_state.messages.append(initial_message)
    
    return workflow_state


# Define routing functions

def route_after_extraction(state: State) -> Literal["assign_sales_person", "__end__"]:
    """Route after lead extraction.
    
    Args:
        state: The current state
        
    Returns:
        Next node to call
    """
    if state.lead_attributes:
        return "assign_sales_person"
    return END


def route_after_assignment(state: State) -> Literal["send_approval", "__end__"]:
    """Route after sales person assignment.
    
    Args:
        state: The current state
        
    Returns:
        Next node to call
    """
    if state.assigned_sales_person:
        return "send_approval"
    return END


def route_after_approval(state: State) -> Literal["create_hubspot_lead", "__end__"]:
    """Route after approval request.
    
    Args:
        state: The current state
        
    Returns:
        Next node to call
    """
    if state.approval_status:
        return "create_hubspot_lead"
    return END


def route_after_hubspot(state: State) -> Literal["notify_sales_person", "__end__"]:
    """Route after Hubspot lead creation.
    
    Args:
        state: The current state
        
    Returns:
        Next node to call
    """
    if state.hubspot_lead_created:
        return "notify_sales_person"
    return END


# Define the workflow graph

def create_graph() -> StateGraph:
    """Create the workflow graph.
    
    Returns:
        The workflow graph
    """
    # Create the graph builder
    builder = StateGraph(State, input=InputState, config_schema=Configuration)
    
    # Add the nodes
    builder.add_node("extract_lead_info", extract_lead_info)
    builder.add_node("assign_sales_person", assign_sales_person_node)
    builder.add_node("send_approval", send_approval_request_node)
    builder.add_node("create_hubspot_lead", create_hubspot_lead_node)
    builder.add_node("notify_sales_person", notify_sales_person_node)
    
    # Add the edges
    builder.add_edge(START, "extract_lead_info")
    builder.add_conditional_edges(
        "extract_lead_info",
        route_after_extraction,
        {
            "assign_sales_person": "assign_sales_person",
            END: END
        }
    )
    builder.add_conditional_edges(
        "assign_sales_person",
        route_after_assignment,
        {
            "send_approval": "send_approval",
            END: END
        }
    )
    builder.add_conditional_edges(
        "send_approval",
        route_after_approval,
        {
            "create_hubspot_lead": "create_hubspot_lead",
            END: END
        }
    )
    builder.add_conditional_edges(
        "create_hubspot_lead",
        route_after_hubspot,
        {
            "notify_sales_person": "notify_sales_person",
            END: END
        }
    )
    builder.add_edge("notify_sales_person", END)
    
    # Add interrupt after approval is sent to wait for manual approval
    # This allows the workflow to pause and wait for human intervention
    graph = builder.compile(
        interrupt_after=["send_approval"]
    )
    
    return graph


# Create the graph
graph = create_graph()


# Define the entry point function
async def process_lead(
    slack_event: Dict[str, Any],
    config: Optional[RunnableConfig] = None
) -> State:
    """Process a lead from a Slack event.
    
    Args:
        slack_event: The Slack event data
        config: Configuration for the workflow
        
    Returns:
        The final state after processing
    """
    # Create the initial state
    initial_state = InputState(
        messages=[],
        slack_event=slack_event
    )
    
    # Run the graph
    final_state = await graph.ainvoke(initial_state, config)
    
    return final_state
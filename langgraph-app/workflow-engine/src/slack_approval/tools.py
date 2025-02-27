"""This module provides tools for processing leads from Slack.

It includes tools for extracting lead information, assigning sales people,
sending approval requests, creating leads in Hubspot, and notifying users.
"""

from typing import Any, Callable, Dict, List, Optional
from typing_extensions import Annotated

from langchain_core.tools import BaseTool, StructuredTool, Tool, tool
from langchain_core.runnables import RunnableConfig
from slack_approval.configuration import Configuration
from slack_approval.state import LeadAttributes


@tool
async def extract_lead_attributes(slack_message: str) -> Dict[str, str]:
    """Extract key attributes from a lead message.
    
    Args:
        slack_message: The message content from Slack
        
    Returns:
        A dictionary with extracted lead attributes (geo_location, industry, engagement)
    """
    # In a real implementation, this would use an LLM or other extraction method
    # For demo purposes, we'll simulate extraction
    print(f"Extracting lead attributes from: {slack_message}")
    
    # Simulate extraction - in production this would be more sophisticated
    return {
        "geo_location": "New York" if "New York" in slack_message else "CA",
        "industry": "Insurance" if "Insurance" in slack_message else "Automobile",
        "engagement": "services"
    }


@tool
async def assign_sales_person(geo_location: str, industry: str, engagement: str) -> str:
    """Assign a sales person based on lead criteria.
    
    Args:
        geo_location: Geographic location of the lead
        industry: Industry of the lead
        engagement: Type of engagement
        
    Returns:
        The name of the assigned sales person
    """
    # Assignment logic based on criteria
    if geo_location == "New York" and industry == "Insurance" and engagement == "services":
        return "Edward"
    elif geo_location == "CA" and industry == "Automobile" and engagement == "services":
        return "John"
    else:
        return "Sales Team" # Default assignment


@tool
async def send_approval_request(
    lead_attributes: Dict[str, str], 
    assigned_person: str, 
    *, 
    config: Annotated[RunnableConfig, "InjectedToolArg"]
) -> bool:
    """Send an approval request to the admin.
    
    Args:
        lead_attributes: The extracted lead attributes
        assigned_person: The assigned sales person
        config: The configuration for the tool
        
    Returns:
        True if the approval request was sent successfully
    """
    configuration = Configuration.from_runnable_config(config)
    
    # In a real implementation, this would send an email or Slack message
    print(f"Sending approval request for lead assignment to {assigned_person}")
    print(f"Lead attributes: {lead_attributes}")
    
    # Simulate sending approval request
    return configuration.should_send_approval_request


@tool
async def create_hubspot_lead(
    lead_attributes: Dict[str, str], 
    assigned_person: str
) -> bool:
    """Create a lead in Hubspot.
    
    Args:
        lead_attributes: The extracted lead attributes
        assigned_person: The assigned sales person
        
    Returns:
        True if the lead was created successfully
    """
    # In a real implementation, this would use the Hubspot API
    print(f"Creating lead in Hubspot with attributes: {lead_attributes}")
    print(f"Assigned to: {assigned_person}")
    
    # Simulate creating lead in Hubspot
    return True


@tool
async def notify_sales_person(assigned_person: str) -> bool:
    """Notify the assigned sales person about the new lead.
    
    Args:
        assigned_person: The assigned sales person
        
    Returns:
        True if the notification was sent successfully
    """
    # In a real implementation, this would send an email or Slack message
    print(f"Notifying {assigned_person} about the new lead assignment")
    
    # Simulate notification
    return True


# List of all available tools
tools = [
    extract_lead_attributes,
    assign_sales_person,
    send_approval_request,
    create_hubspot_lead,
    notify_sales_person
]
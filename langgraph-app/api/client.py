"""Client script to test the Slack lead processing API."""

import asyncio
import json
import httpx
from typing import Dict, Any, Optional

API_URL = "http://localhost:8000"


async def process_lead(slack_event: Dict[str, Any]) -> Dict[str, Any]:
    """Process a lead from Slack.
    
    Args:
        slack_event: The Slack event data
        
    Returns:
        API response
    """
    async with httpx.AsyncClient(timeout=30.0) as client:  
        response = await client.post(
            f"{API_URL}/api/slack/lead",
            json=slack_event
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
        return response.json()


async def approve_lead(thread_id: str, approved: bool) -> Dict[str, Any]:
    """Approve or reject a lead assignment.
    
    Args:
        thread_id: The thread ID
        approved: Whether to approve the lead
        
    Returns:
        API response
    """
    async with httpx.AsyncClient(timeout=30.0) as client:  
        response = await client.post(
            f"{API_URL}/api/slack/approve",
            json={
                "thread_id": thread_id,
                "approved": approved
            }
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
        return response.json()


async def get_thread_status(thread_id: str) -> Dict[str, Any]:
    """Get the status of a workflow thread.
    
    Args:
        thread_id: The thread ID
        
    Returns:
        API response
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/slack/thread/{thread_id}"
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
        return response.json()


async def run_demo():
    """Run a demo of the Slack lead processing workflow."""
    # Sample Slack event
    slack_event = {
        "event": "message",
        "user": {
            "id": "U123456",
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        "slack_message": {
            "text": "Hi, I'm interested in your product. I work for a healthcare company in New York and we're looking for a solution to manage our patient data. We have about 500 employees and are growing rapidly.",
            "channel": "C123456",
            "ts": "1234567890.123456"
        }
    }
    
    # Process the lead
    print("Processing lead...")
    lead_response = await process_lead(slack_event)
    
    if not lead_response:
        print("Failed to process lead")
        return
    
    print(f"Lead processed. Thread ID: {lead_response['thread_id']}")
    print(f"Status: {lead_response['status']}")
    print(f"Lead attributes: {json.dumps(lead_response['lead_attributes'], indent=2)}")
    print(f"Assigned sales person: {lead_response['assigned_sales_person']}")
    print(f"Requires approval: {lead_response['requires_approval']}")
    
    # Get the thread status
    print("\nGetting thread status...")
    thread_status = await get_thread_status(lead_response['thread_id'])
    
    if not thread_status:
        print("Failed to get thread status")
        return
    
    print(f"Thread status: {thread_status['status']}")
    
    # Wait a moment to ensure the workflow has settled
    print("\nWaiting for 3 seconds before approving...")
    await asyncio.sleep(3)
    
    # Approve the lead
    print("Approving lead...")
    approval_response = await approve_lead(lead_response['thread_id'], True)
    
    if not approval_response:
        print("Failed to approve lead")
        return
    
    print(f"Lead approved. Status: {approval_response['status']}")
    print(f"Hubspot lead created: {approval_response['hubspot_lead_created']}")
    print(f"Notification sent: {approval_response['notification_sent']}")
    
    # Wait for the workflow to complete after approval
    print("\nWaiting for 5 seconds for workflow to complete...")
    await asyncio.sleep(5)
    
    # Get the final thread status
    print("Getting final thread status...")
    final_status = await get_thread_status(lead_response['thread_id'])
    
    if not final_status:
        print("Failed to get final thread status")
        return
    
    print(f"Final status: {final_status['status']}")
    print(f"Approval status: {final_status['approval_status']}")
    print(f"Hubspot lead created: {final_status['hubspot_lead_created']}")
    print(f"Notification sent: {final_status['notification_sent']}")
    print(f"Messages: {json.dumps(final_status['messages'], indent=2)}")


if __name__ == "__main__":
    asyncio.run(run_demo())

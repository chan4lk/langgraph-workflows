"""FastAPI application for Slack lead processing workflow."""

import os
import json
import httpx
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from langgraph_sdk import get_client


# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Slack Lead Processing API",
    description="API for processing leads from Slack using LangGraph workflows",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangGraph client
client = get_client(url="http://localhost:2024")


# Request models
class SlackEvent(BaseModel):
    """Model for Slack event data."""
    
    event: str = Field(..., description="Event type")
    user: Dict[str, Any] = Field(..., description="User information")
    slack_message: Dict[str, Any] = Field(..., description="Slack message details")
    timestamp: Optional[str] = Field(None, description="Event timestamp")


class ApprovalRequest(BaseModel):
    """Model for approval request."""
    
    thread_id: str = Field(..., description="Thread ID of the workflow")
    approved: bool = Field(..., description="Whether the lead assignment is approved")


class WorkflowResponse(BaseModel):
    """Model for workflow response."""
    
    thread_id: str = Field(..., description="Thread ID of the workflow")
    status: str = Field(..., description="Current status of the workflow")
    lead_attributes: Optional[Dict[str, Any]] = Field(None, description="Extracted lead attributes")
    assigned_sales_person: Optional[str] = Field(None, description="Assigned sales person")
    approval_status: Optional[bool] = Field(None, description="Approval status")
    hubspot_lead_created: Optional[bool] = Field(None, description="Whether the lead was created in Hubspot")
    notification_sent: Optional[bool] = Field(None, description="Whether notification was sent to sales person")
    messages: List[str] = Field(default_factory=list, description="Workflow messages")
    requires_approval: bool = Field(False, description="Whether the workflow requires approval")


def extract_state_values(state_values: Any) -> Dict[str, Any]:
    """Extract relevant values from the state.
    
    Args:
        state_values: The state values from LangGraph
        
    Returns:
        Extracted values in a standardized format
    """
    # Initialize default result
    result = {
        "lead_attributes": None,
        "assigned_sales_person": None,
        "approval_status": None,
        "hubspot_lead_created": False,
        "notification_sent": False,
        "messages": []
    }
    
    # Handle case where state_values is not a dict
    if callable(state_values):
        print("Warning: state_values is callable, not a dict")
        return result
    
    if not state_values or not isinstance(state_values, dict):
        print(f"Warning: state_values is not a dict: {type(state_values)}")
        return result
    
    # Extract messages
    if "messages" in state_values:
        if isinstance(state_values["messages"], list):
            result["messages"] = [
                msg.get("content", "") if isinstance(msg, dict) else str(msg)
                for msg in state_values["messages"]
            ]
    
    # Extract lead attributes
    if "lead_attributes" in state_values:
        lead_attrs = state_values["lead_attributes"]
        if lead_attrs and isinstance(lead_attrs, dict):
            result["lead_attributes"] = {
                "geo_location": lead_attrs.get("geo_location"),
                "industry": lead_attrs.get("industry"),
                "engagement": lead_attrs.get("engagement")
            }
    
    # Extract other fields
    if "assigned_sales_person" in state_values:
        result["assigned_sales_person"] = state_values["assigned_sales_person"]
    
    # Handle approval_status with special care
    if "approval_status" in state_values:
        # Convert to boolean if it's a string
        if isinstance(state_values["approval_status"], str):
            result["approval_status"] = state_values["approval_status"].lower() == "true"
        else:
            result["approval_status"] = bool(state_values["approval_status"])
        print(f"Extracted approval_status: {result['approval_status']} (original: {state_values['approval_status']})")
    
    if "hubspot_lead_created" in state_values:
        if isinstance(state_values["hubspot_lead_created"], str):
            result["hubspot_lead_created"] = state_values["hubspot_lead_created"].lower() == "true"
        else:
            result["hubspot_lead_created"] = bool(state_values["hubspot_lead_created"])
    
    if "notification_sent" in state_values:
        if isinstance(state_values["notification_sent"], str):
            result["notification_sent"] = state_values["notification_sent"].lower() == "true"
        else:
            result["notification_sent"] = bool(state_values["notification_sent"])
    
    return result


@app.post("/api/slack/lead", response_model=WorkflowResponse)
async def process_slack_lead(slack_event: SlackEvent, background_tasks: BackgroundTasks):
    """Process a lead from Slack.
    
    Args:
        slack_event: The Slack event data
        background_tasks: FastAPI background tasks
        
    Returns:
        Workflow response with thread ID and status
    """
    try:
        # Create a thread
        thread_response = await client.threads.create()
        thread_id = thread_response["thread_id"]
        print(f"Thread created with ID: {thread_id}")
        
        # Prepare the input
        input_data = {
            "messages": [],
            "slack_event": slack_event.model_dump()
        }
        print(f"Input data: {json.dumps(input_data, indent=2)}")
        
        # Run the workflow until it interrupts after sending approval
        run = await client.runs.create(
            thread_id=thread_id,
            assistant_id="slack_approval",
            input=input_data
            # No need to specify interrupt point as it's configured in the graph
        )
        print(f"Run created: {json.dumps(run, indent=2)}")
        
        # Get the thread state
        try:
            thread_state = await client.threads.get_state(thread_id)
            print(f"Thread state type: {type(thread_state)}")
            print(f"Thread state dir: {dir(thread_state)}")
            
            # Extract values from state
            if hasattr(thread_state, 'values'):
                state_values = thread_state.values
                print("Using thread_state.values")
            elif hasattr(thread_state, 'get_state') and callable(thread_state.get_state):
                state_values = await thread_state.get_state()
                print("Using thread_state.get_state()")
            else:
                state_values = thread_state
                print("Using thread_state directly")
                
            print(f"State values: {json.dumps(state_values, default=str, indent=2)}")
        except Exception as e:
            print(f"Error getting thread state: {str(e)}")
            # Use empty state as fallback
            state_values = {}
        
        extracted_values = extract_state_values(state_values)
        print(f"Extracted values: {json.dumps(extracted_values, indent=2)}")
        
        # Determine status
        status = "awaiting_approval"
        requires_approval = True
        
        # Prepare the response
        response = WorkflowResponse(
            thread_id=thread_id,
            status=status,
            requires_approval=requires_approval,
            messages=extracted_values["messages"],
            lead_attributes=extracted_values["lead_attributes"],
            assigned_sales_person=extracted_values["assigned_sales_person"],
            approval_status=extracted_values["approval_status"],
            hubspot_lead_created=extracted_values["hubspot_lead_created"],
            notification_sent=extracted_values["notification_sent"]
        )
        
        return response
    
    except Exception as e:
        print(f"Error processing lead: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing lead: {str(e)}")


@app.post("/api/slack/approve", response_model=WorkflowResponse)
async def approve_lead(approval_request: ApprovalRequest):
    """Approve or reject a lead assignment.
    
    Args:
        approval_request: The approval request data
        
    Returns:
        Updated workflow response
    """
    thread_id = approval_request.thread_id
    
    try:
        # Check if there are any active runs
        runs = await client.runs.list(thread_id=thread_id)
        print(f"Current runs: {json.dumps(runs, default=str, indent=2)}")
        
        # Find the latest run that's in progress
        active_run_id = None
        if "data" in runs and runs["data"]:
            for run in runs["data"]:
                if run.get("status") in ["in_progress", "queued"]:
                    active_run_id = run.get("run_id")
                    break
        
        if active_run_id:
            print(f"Found active run: {active_run_id}, waiting for it to complete")
            # Wait for the active run to complete
            try:
                result = await client.runs.wait(
                    thread_id=thread_id,
                    run_id=active_run_id,
                    raise_error=True
                )
            except Exception as e:
                print(f"Error waiting for active run: {str(e)}")
                # Continue anyway
        
        # Continue the workflow after approval
        config = {
            "configurable": {
                "approval_status": approval_request.approved
            }
        }
        
        print(f"Approval config: {json.dumps(config, indent=2)}")
        
        # First, update the thread state directly to set approval_status
        try:
            # Get current state
            thread_state = await client.threads.get_state(thread_id)
            
            # Extract values from state
            if hasattr(thread_state, 'values'):
                state_values = thread_state.values
            elif hasattr(thread_state, 'get_state') and callable(thread_state.get_state):
                state_values = await thread_state.get_state()
            else:
                state_values = thread_state
                
            # Update approval_status
            state_values["approval_status"] = approval_request.approved
            
            # Set the updated state
            await client.threads.set_state(thread_id, state_values)
            print(f"Updated thread state with approval_status: {approval_request.approved}")
        except Exception as e:
            print(f"Error updating thread state: {str(e)}")
        
        # Create a new run to continue the workflow
        try:
            run = await client.runs.create(
                thread_id=thread_id,
                assistant_id="slack_approval",
                config=config
            )
            
            # Wait for the run to complete
            result = await client.runs.wait(
                thread_id=thread_id,
                run_id=run["run_id"],
                raise_error=True
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                # Conflict - there's already a run in progress
                print("Conflict detected - there's already a run in progress")
                # Get the latest run
                runs = await client.runs.list(thread_id=thread_id)
                if "data" in runs and runs["data"]:
                    latest_run = runs["data"][0]
                    latest_run_id = latest_run.get("run_id")
                    if latest_run_id:
                        print(f"Waiting for latest run: {latest_run_id}")
                        result = await client.runs.wait(
                            thread_id=thread_id,
                            run_id=latest_run_id,
                            raise_error=True
                        )
            else:
                raise
        
        # Get the thread state
        try:
            thread_state = await client.threads.get_state(thread_id)
            
            # Extract values from state
            if hasattr(thread_state, 'values'):
                state_values = thread_state.values
            elif hasattr(thread_state, 'get_state') and callable(thread_state.get_state):
                state_values = await thread_state.get_state()
            else:
                state_values = thread_state
        except Exception as e:
            print(f"Error getting thread state: {str(e)}")
            # Use empty state as fallback
            state_values = {}
            
        extracted_values = extract_state_values(state_values)
        
        # Force the approval status to match the request
        extracted_values["approval_status"] = approval_request.approved
        
        # Determine status
        status = "completed" if approval_request.approved else "rejected"
        requires_approval = False
        
        # Prepare the response
        response = WorkflowResponse(
            thread_id=thread_id,
            status=status,
            requires_approval=requires_approval,
            messages=extracted_values["messages"],
            lead_attributes=extracted_values["lead_attributes"],
            assigned_sales_person=extracted_values["assigned_sales_person"],
            approval_status=extracted_values["approval_status"],
            hubspot_lead_created=extracted_values["hubspot_lead_created"],
            notification_sent=extracted_values["notification_sent"]
        )
        
        return response
    
    except Exception as e:
        print(f"Error processing approval: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing approval: {str(e)}")


@app.get("/api/slack/thread/{thread_id}", response_model=WorkflowResponse)
async def get_thread_status(thread_id: str):
    """Get the status of a workflow thread.
    
    Args:
        thread_id: The thread ID
        
    Returns:
        Current workflow response
    """
    try:
        # Get the thread state
        try:
            thread_state = await client.threads.get_state(thread_id)
            
            # Extract values from state
            if hasattr(thread_state, 'values'):
                state_values = thread_state.values
            elif hasattr(thread_state, 'get_state') and callable(thread_state.get_state):
                state_values = await thread_state.get_state()
            else:
                state_values = thread_state
        except Exception as e:
            print(f"Error getting thread state: {str(e)}")
            # Use empty state as fallback
            state_values = {}
            
        extracted_values = extract_state_values(state_values)
        
        # Determine status and approval requirement
        status = "completed"
        requires_approval = False
        
        if extracted_values["approval_status"] is None:
            status = "awaiting_approval"
            requires_approval = True
        elif extracted_values["approval_status"] is False:
            status = "rejected"
        
        # Prepare the response
        response = WorkflowResponse(
            thread_id=thread_id,
            status=status,
            requires_approval=requires_approval,
            messages=extracted_values["messages"],
            lead_attributes=extracted_values["lead_attributes"],
            assigned_sales_person=extracted_values["assigned_sales_person"],
            approval_status=extracted_values["approval_status"],
            hubspot_lead_created=extracted_values["hubspot_lead_created"],
            notification_sent=extracted_values["notification_sent"]
        )
        
        return response
    
    except Exception as e:
        print(f"Error getting thread status: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error getting thread status: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

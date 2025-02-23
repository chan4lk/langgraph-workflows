from fastapi import APIRouter, HTTPException, Request
from typing import List
from datetime import datetime
import sys
import os
import logging
import json
from pydantic import ValidationError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import Workflow
from utils.file_operations import load_workflows, save_workflows

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/workflows",
    tags=["workflows"]
)

@router.get("", response_model=List[Workflow])
async def list_workflows():
    """List all workflows"""
    try:
        workflows = load_workflows()
        return [Workflow(**w) if isinstance(w, dict) else w for w in workflows]
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID"""
    try:
        workflows = load_workflows()
        workflow = next((w for w in workflows if w["id"] == workflow_id), None)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return Workflow(**workflow)
    except Exception as e:
        logger.error(f"Error getting workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=Workflow)
async def create_workflow(workflow: Workflow):
    """Create a new workflow"""
    try:
        workflows = load_workflows()
        
        # Check if workflow with same ID exists
        if any(w["id"] == workflow.id for w in workflows):
            raise HTTPException(status_code=400, detail="Workflow with this ID already exists")
        
        workflow_dict = workflow.dict(exclude_none=True)
        workflows.append(workflow_dict)
        save_workflows(workflows)
        return workflow
    except ValidationError as e:
        logger.error(f"Validation error details: {e.errors()}")
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Validation error",
                "errors": e.errors()
            }
        )
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: str, request: Request):
    """Update an existing workflow or create if it doesn't exist"""
    try:
        # Log raw request body
        body = await request.json()
        
        # Try to create Workflow model
        workflow = Workflow(**body)
        
        workflows = load_workflows()
        
        # Update timestamp
        workflow.updatedAt = datetime.utcnow().isoformat()
        
        # Convert to dict for JSON serialization, excluding None values
        workflow_dict = workflow.dict(exclude_none=True)
        logger.info(f"Processed workflow data: {json.dumps(workflow_dict, indent=2)}")
        
        # Find and update the workflow
        for i, existing in enumerate(workflows):
            if existing["id"] == workflow_id:
                workflows[i] = workflow_dict
                save_workflows(workflows)
                return workflow
        
        # If not found, create new
        workflows.append(workflow_dict)
        save_workflows(workflows)
        return workflow
        
    except ValidationError as e:
        logger.error(f"Validation error details: {e.errors()}")
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Validation error",
                "errors": e.errors()
            }
        )
    except Exception as e:
        logger.error(f"Error updating workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow"""
    try:
        workflows = load_workflows()
        
        filtered_workflows = [w for w in workflows if w["id"] != workflow_id]
        if len(filtered_workflows) == len(workflows):
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        save_workflows(filtered_workflows)
        return {"message": "Workflow deleted successfully"}
    except ValidationError as e:
        logger.error(f"Validation error details: {e.errors()}")
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Validation error",
                "errors": e.errors()
            }
        )
    except Exception as e:
        logger.error(f"Error deleting workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

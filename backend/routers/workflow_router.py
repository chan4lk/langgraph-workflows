from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from backend.models.models import Workflow
from backend.utils.file_operations import load_workflows, save_workflows

router = APIRouter(
    prefix="/api/workflows",
    tags=["workflows"]
)

@router.get("", response_model=List[Workflow])
async def list_workflows():
    """List all workflows"""
    return load_workflows()

@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID"""
    workflows = load_workflows()
    workflow = next((w for w in workflows if w["id"] == workflow_id), None)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.post("", response_model=Workflow)
async def create_workflow(workflow: Workflow):
    """Create a new workflow"""
    workflows = load_workflows()
    
    # Check if workflow with same ID exists
    if any(w["id"] == workflow.id for w in workflows):
        raise HTTPException(status_code=400, detail="Workflow with this ID already exists")
    
    workflow_dict = workflow.dict()
    workflows.append(workflow_dict)
    save_workflows(workflows)
    return workflow_dict

@router.put("/{workflow_id}")
async def update_workflow(workflow_id: str, workflow: Workflow):
    """Update an existing workflow or create if it doesn't exist"""
    workflows = load_workflows()
    
    # Update timestamp
    workflow.updatedAt = datetime.utcnow().isoformat()
    
    # Convert to dict for JSON serialization
    workflow_dict = workflow.dict(exclude_none=True)
    
    # Find and update the workflow
    for i, existing in enumerate(workflows):
        if existing["id"] == workflow_id:
            # Preserve existing fields that might not be in the update
            existing.update(workflow_dict)
            workflows[i] = existing
            save_workflows(workflows)
            return existing
    
    # If not found, create new
    workflows.append(workflow_dict)
    save_workflows(workflows)
    return workflow_dict

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow"""
    workflows = load_workflows()
    
    filtered_workflows = [w for w in workflows if w["id"] != workflow_id]
    if len(filtered_workflows) == len(workflows):
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    save_workflows(filtered_workflows)
    return {"message": "Workflow deleted successfully"}

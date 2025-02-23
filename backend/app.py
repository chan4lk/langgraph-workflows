from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os
from pathlib import Path

app = FastAPI(title="Workflow Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage path
DATA_DIR = Path("data")
WORKFLOWS_FILE = DATA_DIR / "workflows.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Ensure workflows.json exists with empty array if it doesn't exist
if not WORKFLOWS_FILE.exists():
    with open(WORKFLOWS_FILE, "w") as f:
        json.dump([], f)

# Models
class Position(BaseModel):
    x: float
    y: float

class NodeData(BaseModel):
    label: str
    description: Optional[str] = None
    agentName: Optional[str] = None
    llmConfigId: Optional[str] = None
    taskName: Optional[str] = None
    assignmentRules: Optional[Dict[str, List[str]]] = None
    workflowId: Optional[str] = None

class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: NodeData
    draggable: bool = True

class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: str = "default"
    data: Optional[Dict[str, Any]] = None

class Workflow(BaseModel):
    id: str
    name: str
    description: str
    version: str
    nodes: List[Node]
    edges: List[Edge]
    createdAt: str
    updatedAt: str

# Helper functions
def load_workflows():
    try:
        with open(WORKFLOWS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_workflows(workflows):
    with open(WORKFLOWS_FILE, "w") as f:
        json.dump(workflows, f, indent=2)

# API endpoints
@app.get("/api/workflows", response_model=List[Workflow])
async def list_workflows():
    """List all workflows"""
    return load_workflows()

@app.get("/api/workflows/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID"""
    workflows = load_workflows()
    workflow = next((w for w in workflows if w["id"] == workflow_id), None)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@app.post("/api/workflows", response_model=Workflow)
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

@app.put("/api/workflows/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: str, workflow: Workflow):
    """Update an existing workflow or create if it doesn't exist"""
    workflows = load_workflows()
    
    index = next((i for i, w in enumerate(workflows) if w["id"] == workflow_id), None)
    workflow_dict = workflow.dict()
    workflow_dict["updatedAt"] = datetime.utcnow().isoformat()
    
    if index is None:
        # If workflow doesn't exist, create it
        workflows.append(workflow_dict)
    else:
        # Update existing workflow
        workflows[index] = workflow_dict
    
    save_workflows(workflows)
    return workflow_dict

@app.delete("/api/workflows/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow"""
    workflows = load_workflows()
    
    filtered_workflows = [w for w in workflows if w["id"] != workflow_id]
    if len(filtered_workflows) == len(workflows):
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    save_workflows(filtered_workflows)
    return {"message": "Workflow deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

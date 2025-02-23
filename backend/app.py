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

# Data storage paths
DATA_DIR = Path("data")
WORKFLOWS_FILE = DATA_DIR / "workflows.json"
TEMPLATES_FILE = DATA_DIR / "templates.json"

# Ensure data directory and files exist
DATA_DIR.mkdir(exist_ok=True)
if not WORKFLOWS_FILE.exists():
    with open(WORKFLOWS_FILE, "w") as f:
        json.dump([], f)
if not TEMPLATES_FILE.exists():
    with open(TEMPLATES_FILE, "w") as f:
        json.dump([], f)

# Models
class Position(BaseModel):
    x: float
    y: float

class PromptTemplate(BaseModel):
    id: str
    name: str
    content: str
    description: Optional[str] = None
    createdAt: str
    updatedAt: str

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

def load_templates():
    try:
        with open(TEMPLATES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_templates(templates):
    with open(TEMPLATES_FILE, "w") as f:
        json.dump(templates, f, indent=2)

# Workflow API endpoints
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

# Prompt Template API endpoints
@app.get("/api/templates", response_model=List[PromptTemplate])
async def list_templates():
    """List all prompt templates"""
    return load_templates()

@app.get("/api/templates/{template_id}", response_model=PromptTemplate)
async def get_template(template_id: str):
    """Get a specific prompt template by ID"""
    templates = load_templates()
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.post("/api/templates", response_model=PromptTemplate)
async def create_template(template: PromptTemplate):
    """Create a new prompt template"""
    templates = load_templates()
    
    # Check if template with same ID exists
    if any(t["id"] == template.id for t in templates):
        raise HTTPException(status_code=400, detail="Template with this ID already exists")
    
    template_dict = template.dict()
    template_dict["createdAt"] = datetime.utcnow().isoformat()
    template_dict["updatedAt"] = template_dict["createdAt"]
    
    templates.append(template_dict)
    save_templates(templates)
    return template_dict

@app.put("/api/templates/{template_id}", response_model=PromptTemplate)
async def update_template(template_id: str, template: PromptTemplate):
    """Update an existing prompt template"""
    templates = load_templates()
    
    index = next((i for i, t in enumerate(templates) if t["id"] == template_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template_dict = template.dict()
    template_dict["updatedAt"] = datetime.utcnow().isoformat()
    templates[index] = template_dict
    
    save_templates(templates)
    return template_dict

@app.delete("/api/templates/{template_id}")
async def delete_template(template_id: str):
    """Delete a prompt template"""
    templates = load_templates()
    
    filtered_templates = [t for t in templates if t["id"] != template_id]
    if len(filtered_templates) == len(templates):
        raise HTTPException(status_code=404, detail="Template not found")
    
    save_templates(filtered_templates)
    return {"message": "Template deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

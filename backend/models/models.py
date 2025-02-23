from pydantic import BaseModel
from typing import List, Optional, Dict, Any

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

class Tool(BaseModel):
    id: str
    name: str
    description: str
    type: str
    config: Optional[Dict[str, Any]] = None

class NodeData(BaseModel):
    label: str
    description: Optional[str] = None
    # Agent specific fields
    agentName: Optional[str] = None
    llmConfigId: Optional[str] = None
    promptTemplateId: Optional[str] = None
    template: Optional[PromptTemplate] = None
    tools: Optional[List[Tool]] = None
    # Function specific fields
    functionName: Optional[str] = None
    # Human task specific fields
    taskName: Optional[str] = None
    assignmentRules: Optional[Dict[str, List[str]]] = None
    inputFields: Optional[List[Dict[str, Any]]] = None
    # Sub-workflow specific fields
    workflowId: Optional[str] = None
    parameterMapping: Optional[Dict[str, str]] = None

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

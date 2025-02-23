from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Literal
from enum import Enum

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

class ToolType(str, Enum):
    API = "api"
    CODE_BLOCK = "code_block"

class APIParameter(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    required: bool = True
    default: Optional[Any] = None

class APIToolConfig(BaseModel):
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    url: str
    headers: Optional[Dict[str, str]] = None
    parameters: List[APIParameter] = []
    request_body_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None

class CodeBlockConfig(BaseModel):
    function_name: str
    code: str
    parameters: List[APIParameter] = []
    return_type: Optional[str] = None
    description: Optional[str] = None

class ToolConfig(BaseModel):
    type: ToolType
    api_config: Optional[APIToolConfig] = None
    code_block_config: Optional[CodeBlockConfig] = None

    @property
    def config(self) -> Union[APIToolConfig, CodeBlockConfig, None]:
        if self.type == ToolType.API:
            return self.api_config
        elif self.type == ToolType.CODE_BLOCK:
            return self.code_block_config
        return None

class Tool(BaseModel):
    id: str
    name: str
    description: str
    type: str
    config: Optional[Dict[str, Any]] = None

class MCPTool(BaseModel):
    id: str
    name: str
    description: str
    type: ToolType
    config: ToolConfig
    createdAt: str
    updatedAt: str

class NodeType(str, Enum):
    START = "start"
    END = "end"
    AGENT = "agent"
    FUNCTION = "function"
    HUMAN_TASK = "human_task"
    TOOL = "tool"
    SUB_WORKFLOW = "sub_workflow"
    FORK = "fork"
    JOIN = "join"

class NodeData(BaseModel):
    label: str
    description: Optional[str] = None
    type: NodeType
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
    # Tool specific fields
    toolId: Optional[str] = None
    toolConfig: Optional[ToolConfig] = None

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

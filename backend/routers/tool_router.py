from fastapi import APIRouter, HTTPException
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import MCPTool, ToolType, APIToolConfig, CodeBlockConfig, APIParameter
from utils.file_operations import load_tools, save_tools
from datetime import datetime

router = APIRouter(
    prefix="/api/tools",
    tags=["tools"]
)

@router.get("", response_model=List[MCPTool])
async def list_tools():
    """List all MCP tools"""
    tools = load_tools()
    
    # Convert dict to MCPTool model with parameter validation
    mcp_tools = []
    for tool in tools:
        if isinstance(tool, dict):
            # Convert request_body_schema to parameters if present
            config = tool.get("config", {})
            api_config = config.get("api_config", {})
            if schema := api_config.get("request_body_schema"):
                api_config["parameters"] = APIParameter.from_json_schema(schema)
            mcp_tools.append(MCPTool(**tool))
        else:
            mcp_tools.append(tool)
    
    return mcp_tools

@router.get("/{tool_id}", response_model=MCPTool)
async def get_tool(tool_id: str):
    """Get a specific tool by ID"""
    tools = load_tools()
    tool = next((t for t in tools if t["id"] == tool_id), None)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return MCPTool(**tool)

@router.post("", response_model=MCPTool)
async def create_tool(tool: MCPTool):
    """Create a new tool"""
    tools = load_tools()
    
    # Check if tool with same ID exists
    if any(t["id"] == tool.id for t in tools):
        raise HTTPException(status_code=400, detail="Tool with this ID already exists")
    
    # Validate tool configuration based on type
    if tool.type == ToolType.API and not tool.config.api_config:
        raise HTTPException(status_code=400, detail="API tool must have api_config")
    elif tool.type == ToolType.CODE_BLOCK and not tool.config.code_block_config:
        raise HTTPException(status_code=400, detail="Code block tool must have code_block_config")
    
    tool_dict = tool.dict()
    tools.append(tool_dict)
    save_tools(tools)
    return tool

@router.put("/{tool_id}", response_model=MCPTool)
async def update_tool(tool_id: str, tool: MCPTool):
    """Update an existing tool"""
    tools = load_tools()
    
    # Validate tool configuration based on type
    if tool.type == ToolType.API and not tool.config.api_config:
        raise HTTPException(status_code=400, detail="API tool must have api_config")
    elif tool.type == ToolType.CODE_BLOCK and not tool.config.code_block_config:
        raise HTTPException(status_code=400, detail="Code block tool must have code_block_config")
    
    # Update timestamp
    tool.updatedAt = datetime.utcnow().isoformat()
    tool_dict = tool.dict()
    
    # Find and update the tool
    for i, existing in enumerate(tools):
        if existing["id"] == tool_id:
            tools[i] = tool_dict
            save_tools(tools)
            return tool
    
    # If not found, create new
    tools.append(tool_dict)
    save_tools(tools)
    return tool

@router.delete("/{tool_id}")
async def delete_tool(tool_id: str):
    """Delete a tool"""
    tools = load_tools()
    
    filtered_tools = [t for t in tools if t["id"] != tool_id]
    if len(filtered_tools) == len(tools):
        raise HTTPException(status_code=404, detail="Tool not found")
    
    save_tools(filtered_tools)
    return {"message": "Tool deleted successfully"}

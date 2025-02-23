from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from backend.models.models import MCPTool
from backend.utils.file_operations import load_tools, save_tools

router = APIRouter(
    prefix="/api/tools",
    tags=["tools"]
)

@router.get("", response_model=List[MCPTool])
async def list_tools():
    """List all MCP tools"""
    return load_tools()

@router.get("/{tool_id}", response_model=MCPTool)
async def get_tool(tool_id: str):
    """Get a specific tool by ID"""
    tools = load_tools()
    tool = next((t for t in tools if t["id"] == tool_id), None)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.post("", response_model=MCPTool)
async def create_tool(tool: MCPTool):
    """Create a new tool"""
    tools = load_tools()
    
    # Check if tool with same ID exists
    if any(t["id"] == tool.id for t in tools):
        raise HTTPException(status_code=400, detail="Tool with this ID already exists")
    
    tool_dict = tool.dict()
    tools.append(tool_dict)
    save_tools(tools)
    return tool_dict

@router.put("/{tool_id}", response_model=MCPTool)
async def update_tool(tool_id: str, tool: MCPTool):
    """Update an existing tool"""
    tools = load_tools()
    
    # Update timestamp
    tool.updatedAt = datetime.utcnow().isoformat()
    tool_dict = tool.dict()
    
    # Find and update the tool
    for i, existing in enumerate(tools):
        if existing["id"] == tool_id:
            tools[i] = tool_dict
            save_tools(tools)
            return tool_dict
    
    # If not found, create new
    tools.append(tool_dict)
    save_tools(tools)
    return tool_dict

@router.delete("/{tool_id}")
async def delete_tool(tool_id: str):
    """Delete a tool"""
    tools = load_tools()
    
    filtered_tools = [t for t in tools if t["id"] != tool_id]
    if len(filtered_tools) == len(tools):
        raise HTTPException(status_code=404, detail="Tool not found")
    
    save_tools(filtered_tools)
    return {"message": "Tool deleted successfully"}

import json
from pathlib import Path
import os
from datetime import datetime

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent
DATA_DIR = BACKEND_DIR / "data"
MCP_TOOLS_DIR = BACKEND_DIR / "mcp_tools_server"
WORKFLOWS_FILE = DATA_DIR / "workflows.json"
TEMPLATES_FILE = DATA_DIR / "templates.json"
TOOLS_FILE = MCP_TOOLS_DIR / "tools.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MCP_TOOLS_DIR.mkdir(exist_ok=True)

def initialize_json_file(file_path: Path, initial_data=None):
    """Initialize a JSON file with default data if it doesn't exist"""
    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump(initial_data if initial_data is not None else [], f, indent=2)
    elif file_path.stat().st_size == 0:  # File exists but is empty
        with open(file_path, "w") as f:
            json.dump(initial_data if initial_data is not None else [], f, indent=2)

# Initialize files with empty arrays if they don't exist
initialize_json_file(WORKFLOWS_FILE)
initialize_json_file(TEMPLATES_FILE)
initialize_json_file(TOOLS_FILE, {"tools": []})

def load_workflows():
    """Load workflows from the JSON file"""
    initialize_json_file(WORKFLOWS_FILE)  # Ensure file exists and is properly initialized
    try:
        with open(WORKFLOWS_FILE, "r") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading workflows: {e}")  # Debug print
        return []

def save_workflows(workflows):
    """Save workflows to the JSON file"""
    try:
        with open(WORKFLOWS_FILE, "w") as f:
            json.dump(workflows, f, indent=2)
    except Exception as e:
        print(f"Error saving workflows: {e}")  # Debug print
        raise

def load_templates():
    """Load templates from the JSON file"""
    initialize_json_file(TEMPLATES_FILE)  # Ensure file exists and is properly initialized
    try:
        with open(TEMPLATES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_templates(templates):
    """Save templates to the JSON file"""
    with open(TEMPLATES_FILE, "w") as f:
        json.dump(templates, f, indent=2)

def load_tools():
    """Load MCP tools from the JSON file"""
    initialize_json_file(TOOLS_FILE, {"tools": []})  # Initialize with proper structure
    try:
        with open(TOOLS_FILE, "r") as f:
            data = json.load(f)
            tools_data = data.get("tools", [])
            
            # Convert tools to proper format with required fields
            formatted_tools = []
            for tool in tools_data:
                formatted_tool = {
                    "id": tool.get("name", "").lower().replace(" ", "-"),  # Generate ID from name
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "type": "api",  # Default to API type
                    "config": {
                        "type": "api",
                        "api_config": {
                            "method": "POST",
                            "url": "",
                            "parameters": [],
                            "request_body_schema": tool.get("parameters", {})
                        }
                    },
                    "createdAt": tool.get("createdAt", datetime.now().isoformat()),
                    "updatedAt": tool.get("updatedAt", datetime.now().isoformat())
                }
                formatted_tools.append(formatted_tool)
            
            return formatted_tools
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading tools: {e}")
        return []

def save_tools(tools):
    """Save MCP tools to the JSON file"""
    try:
        with open(TOOLS_FILE, "w") as f:
            json.dump({"tools": tools}, f, indent=2)
    except Exception as e:
        print(f"Error saving tools: {e}")  # Debug print
        raise

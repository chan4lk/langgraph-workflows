"""
Output parsers for the meta prompter Windsurf workflow.
"""
from typing import Dict, List, Any
import json
from langchain_core.output_parsers import JsonOutputParser


# Simple JSON output parser for requirements
requirements_parser = JsonOutputParser()


# Parser for UI flows with fallback
def ui_flow_parser(output: str) -> List[Dict[str, Any]]:
    """
    Parse UI flow output from LLM.
    
    Args:
        output (str): LLM output string
        
    Returns:
        List[Dict]: List of UI flow objects
    """
    try:
        # Try to parse as JSON
        return json.loads(output)
    except json.JSONDecodeError:
        # Fallback: Extract JSON-like content
        try:
            # Look for array pattern
            start_idx = output.find('[')
            end_idx = output.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = output[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                # Return empty list as fallback
                return []
        except Exception:
            # Last resort fallback
            return []


# Parser for UI prompts with fallback
def ui_prompt_parser(output: str) -> List[str]:
    """
    Parse UI prompt output from LLM.
    
    Args:
        output (str): LLM output string
        
    Returns:
        List[str]: List of UI prompt strings
    """
    try:
        # Try to parse as JSON
        parsed = json.loads(output)
        if isinstance(parsed, list):
            return parsed
        else:
            # If it's not a list, wrap it
            return [output]
    except json.JSONDecodeError:
        # Fallback: Split by newlines and filter empty lines
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        return lines


# Parser for architecture prompts with fallback
def architecture_prompt_parser(output: str) -> List[Dict[str, Any]]:
    """
    Parse architecture prompt output from LLM.
    
    Args:
        output (str): LLM output string
        
    Returns:
        List[Dict]: List of architecture prompt objects
    """
    try:
        # Try to parse as JSON
        return json.loads(output)
    except json.JSONDecodeError:
        # Fallback: Extract JSON-like content
        try:
            # Look for array pattern
            start_idx = output.find('[')
            end_idx = output.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = output[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                # Return empty list as fallback
                return []
        except Exception:
            # Last resort fallback
            return []


# Parser for app building prompts with fallback
def app_building_prompt_parser(output: str) -> List[Dict[str, Any]]:
    """
    Parse app building prompt output from LLM.
    
    Args:
        output (str): LLM output string
        
    Returns:
        List[Dict]: List of app building prompt objects
    """
    try:
        # Try to parse as JSON
        return json.loads(output)
    except json.JSONDecodeError:
        # Fallback: Extract JSON-like content
        try:
            # Look for array pattern
            start_idx = output.find('[')
            end_idx = output.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = output[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                # Return empty list as fallback
                return []
        except Exception:
            # Last resort fallback
            return []


# Parser for UI automation prompts with fallback
def ui_automation_prompt_parser(output: str) -> List[Dict[str, Any]]:
    """
    Parse UI automation prompt output from LLM.
    
    Args:
        output (str): LLM output string
        
    Returns:
        List[Dict]: List of UI automation prompt objects
    """
    try:
        # Try to parse as JSON
        return json.loads(output)
    except json.JSONDecodeError:
        # Fallback: Extract JSON-like content
        try:
            # Look for array pattern
            start_idx = output.find('[')
            end_idx = output.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = output[start_idx:end_idx+1]
                return json.loads(json_str)
            else:
                # Return empty list as fallback
                return []
        except Exception:
            # Last resort fallback
            return []

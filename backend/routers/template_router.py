from fastapi import APIRouter, HTTPException
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import PromptTemplate
from utils.file_operations import load_templates, save_templates

router = APIRouter(
    prefix="/api/templates",
    tags=["templates"]
)

@router.get("", response_model=List[PromptTemplate])
async def list_templates():
    """List all prompt templates"""
    return load_templates()

@router.get("/{template_id}", response_model=PromptTemplate)
async def get_template(template_id: str):
    """Get a specific prompt template by ID"""
    templates = load_templates()
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.post("", response_model=PromptTemplate)
async def create_template(template: PromptTemplate):
    """Create a new prompt template"""
    templates = load_templates()
    
    # Check if template with same ID exists
    if any(t["id"] == template.id for t in templates):
        raise HTTPException(status_code=400, detail="Template with this ID already exists")
    
    template_dict = template.dict()
    templates.append(template_dict)
    save_templates(templates)
    return template_dict

@router.put("/{template_id}", response_model=PromptTemplate)
async def update_template(template_id: str, template: PromptTemplate):
    """Update an existing prompt template"""
    templates = load_templates()
    
    for i, existing in enumerate(templates):
        if existing["id"] == template_id:
            template_dict = template.dict()
            templates[i] = template_dict
            save_templates(templates)
            return template_dict
    
    raise HTTPException(status_code=404, detail="Template not found")

@router.delete("/{template_id}")
async def delete_template(template_id: str):
    """Delete a prompt template"""
    templates = load_templates()
    
    filtered_templates = [t for t in templates if t["id"] != template_id]
    if len(filtered_templates) == len(templates):
        raise HTTPException(status_code=404, detail="Template not found")
    
    save_templates(filtered_templates)
    return {"message": "Template deleted successfully"}

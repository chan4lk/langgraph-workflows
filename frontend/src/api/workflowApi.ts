import { Workflow, PromptTemplate } from '../types/workflow';

const API_BASE_URL = 'http://localhost:8000/api';

class WorkflowApi {
  // Workflow methods
  async listWorkflows(): Promise<Workflow[]> {
    const response = await fetch(`${API_BASE_URL}/workflows`);
    if (!response.ok) {
      throw new Error('Failed to fetch workflows');
    }
    return response.json();
  }

  async getWorkflow(id: string): Promise<Workflow> {
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch workflow');
    }
    const workflow = await response.json();
    console.log('Loaded workflow:', JSON.stringify(workflow, null, 2));
    return workflow;
  }

  async createWorkflow(workflow: Workflow): Promise<Workflow> {
    const response = await fetch(`${API_BASE_URL}/workflows`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workflow),
    });
    if (!response.ok) {
      throw new Error('Failed to create workflow');
    }
    return response.json();
  }

  async updateWorkflow(id: string, workflow: Workflow): Promise<Workflow> {
    console.log('Saving workflow:', JSON.stringify(workflow, null, 2));
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workflow),
    });
    if (!response.ok) {
      throw new Error('Failed to update workflow');
    }
    const savedWorkflow = await response.json();
    console.log('Saved workflow response:', JSON.stringify(savedWorkflow, null, 2));
    return savedWorkflow;
  }

  async deleteWorkflow(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete workflow');
    }
  }

  // Template methods
  async listTemplates(): Promise<PromptTemplate[]> {
    const response = await fetch(`${API_BASE_URL}/templates`);
    if (!response.ok) {
      throw new Error('Failed to fetch templates');
    }
    const text = await response.text();
    // Fix malformed JSON array by adding [ at start if missing and removing trailing %
    const cleanedText = text
      .trim()
      .replace(/^(?!\[)/, '[') // Add [ if not present at start
      .replace(/\]%$/, ']'); // Replace ]% with ]
    console.log('Cleaned template response:', cleanedText);
    return JSON.parse(cleanedText);
  }

  async getTemplate(id: string): Promise<PromptTemplate> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch template');
    }
    return response.json();
  }

  async createTemplate(template: Omit<PromptTemplate, 'createdAt' | 'updatedAt'>): Promise<PromptTemplate> {
    const response = await fetch(`${API_BASE_URL}/templates`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(template),
    });
    if (!response.ok) {
      throw new Error('Failed to create template');
    }
    return response.json();
  }

  async updateTemplate(id: string, template: Omit<PromptTemplate, 'createdAt' | 'updatedAt'>): Promise<PromptTemplate> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(template),
    });
    if (!response.ok) {
      throw new Error('Failed to update template');
    }
    return response.json();
  }

  async deleteTemplate(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete template');
    }
  }
}

export const workflowApi = new WorkflowApi();

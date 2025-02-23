import { Workflow } from '../types/workflow';

const API_BASE_URL = 'http://localhost:8000/api';

export const workflowApi = {
  async listWorkflows(): Promise<Workflow[]> {
    const response = await fetch(`${API_BASE_URL}/workflows`);
    if (!response.ok) {
      throw new Error('Failed to fetch workflows');
    }
    return response.json();
  },

  async getWorkflow(id: string): Promise<Workflow> {
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch workflow');
    }
    return response.json();
  },

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
  },

  async updateWorkflow(id: string, workflow: Workflow): Promise<Workflow> {
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
    return response.json();
  },

  async deleteWorkflow(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete workflow');
    }
  },
};

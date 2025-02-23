import { Workflow } from '../types/workflow';
import { Tool } from '../types/tool';
import { API_BASE_URL } from '../config';

const handleApiResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'API request failed');
  }
  const data = await response.json();
  return data;
};

export const workflowApi = {
  async listWorkflows(): Promise<Workflow[]> {
    const response = await fetch(`${API_BASE_URL}/workflows`);
    return handleApiResponse<Workflow[]>(response);
  },

  async getWorkflow(id: string): Promise<Workflow> {
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`);
    return handleApiResponse<Workflow>(response);
  },

  async createWorkflow(workflow: Workflow): Promise<Workflow> {
    const response = await fetch(`${API_BASE_URL}/workflows`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workflow),
    });
    return handleApiResponse<Workflow>(response);
  },

  async updateWorkflow(workflow: Workflow): Promise<Workflow> {
    console.log('Updating workflow:', JSON.stringify(workflow, null, 2));
    const response = await fetch(`${API_BASE_URL}/workflows/${workflow.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workflow),
    });
    return handleApiResponse<Workflow>(response);
  },

  async deleteWorkflow(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/workflows/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to delete workflow');
    }
  },

  async getTools(): Promise<Tool[]> {
    const response = await fetch(`${API_BASE_URL}/tools`);
    return handleApiResponse<Tool[]>(response);
  },

  async getTool(id: string): Promise<Tool> {
    const response = await fetch(`${API_BASE_URL}/tools/${id}`);
    return handleApiResponse<Tool>(response);
  },
};

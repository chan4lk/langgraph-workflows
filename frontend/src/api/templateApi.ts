import { PromptTemplate } from '../types/workflow';
import { API_BASE_URL } from '../config';

const handleApiResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'API request failed');
  }
  const data = await response.json();
  return data;
};

export const templateApi = {
  async listTemplates(): Promise<PromptTemplate[]> {
    const response = await fetch(`${API_BASE_URL}/templates`);
    return handleApiResponse<PromptTemplate[]>(response);
  },

  async getTemplate(id: string): Promise<PromptTemplate> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}`);
    return handleApiResponse<PromptTemplate>(response);
  },

  async createTemplate(template: Omit<PromptTemplate, 'id' | 'createdAt' | 'updatedAt'>): Promise<PromptTemplate> {
    const response = await fetch(`${API_BASE_URL}/templates`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(template),
    });
    return handleApiResponse<PromptTemplate>(response);
  },

  async updateTemplate(id: string, template: Omit<PromptTemplate, 'id' | 'createdAt' | 'updatedAt'>): Promise<PromptTemplate> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(template),
    });
    return handleApiResponse<PromptTemplate>(response);
  },

  async deleteTemplate(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to delete template');
    }
  },
};

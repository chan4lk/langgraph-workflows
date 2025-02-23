export enum ToolType {
  API = 'api',
  CODE_BLOCK = 'code_block',
}

export interface APIParameter {
  name: string;
  type: string;
  description?: string;
  required: boolean;
  default?: any;
}

export interface APIToolConfig {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  url: string;
  headers?: Record<string, string>;
  parameters: APIParameter[];
  request_body_schema?: Record<string, any>;
  response_schema?: Record<string, any>;
}

export interface CodeBlockConfig {
  function_name: string;
  code: string;
  parameters: APIParameter[];
  return_type?: string;
  description?: string;
}

export interface ToolConfig {
  type: ToolType;
  api_config?: APIToolConfig;
  code_block_config?: CodeBlockConfig;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  type: ToolType;
  config: ToolConfig;
  createdAt: string;
  updatedAt: string;
}

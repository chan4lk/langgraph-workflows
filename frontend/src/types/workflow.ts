import { Node, Edge } from 'reactflow';
import { Tool as FullTool, ToolConfig } from './tool';

// Keep in sync with backend NodeType enum
export enum NodeType {
  START = 'start',
  END = 'end',
  AGENT = 'agent',
  FUNCTION = 'function',
  HUMAN_TASK = 'human_task',
  TOOL = 'tool',
  SUB_WORKFLOW = 'sub_workflow',
  FORK = 'fork',
  JOIN = 'join'
}

export type EdgeTypes = 
  | 'default'
  | 'smoothstep'
  | 'step'
  | 'straight';

export interface PromptTemplate {
  id: string;
  name: string;
  content: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

// Simplified Tool type for node data (without timestamps)
export type NodeTool = Omit<FullTool, 'createdAt' | 'updatedAt'>;

export interface NodeData {
  label: string;
  description?: string;
  type: NodeType;
  // Agent specific fields
  agentName?: string;
  llmConfigId?: string;
  promptTemplateId?: string;
  template?: PromptTemplate;
  tools?: NodeTool[];
  // Function specific fields
  functionName?: string;
  // Human task specific fields
  taskName?: string;
  assignmentRules?: Record<string, string[]>;
  inputFields?: any[];
  // Sub-workflow specific fields
  workflowId?: string;
  parameterMapping?: Record<string, string>;
  // Tool specific fields
  toolId?: string;
  toolConfig?: ToolConfig;
  // Fork specific fields
  branches?: string[];
  // Join specific fields
  joinType?: 'all' | 'any';
}

export interface EdgeData {
  conditionExpression?: string;
}

export type WorkflowNode = Node<NodeData>;

export type WorkflowEdge = {
  id: string;
  source: string;
  target: string;
  type: EdgeTypes;
  sourceHandle?: string | null;
  targetHandle?: string | null;
  data?: EdgeData;
};

export interface Workflow {
  id: string;
  name: string;
  description: string;
  version: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  createdAt: string;
  updatedAt: string;
}

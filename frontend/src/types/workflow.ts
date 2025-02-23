import { Node, Edge, EdgeMarker } from 'reactflow';

export type NodeType = 
  | 'start' 
  | 'end' 
  | 'agent' 
  | 'function' 
  | 'human_task' 
  | 'sub_workflow';

export type EdgeType = 
  | 'default'
  | 'conditional'
  | 'fork'
  | 'join';

export interface PromptTemplate {
  id: string;
  name: string;
  content: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  type: 'function' | 'api' | 'custom';
  config?: Record<string, any>;
}

export interface NodeData {
  label: string;
  description?: string;
  // Agent specific fields
  agentName?: string;
  llmConfigId?: string;
  promptTemplateId?: string;
  template?: PromptTemplate | null;
  tools?: Tool[];
  // Function specific fields
  functionName?: string;
  // Human task specific fields
  taskName?: string;
  assignmentRules?: {
    users?: string[];
    groups?: string[];
  };
  inputFields?: {
    name: string;
    type: string;
    required: boolean;
  }[];
  // Sub-workflow specific fields
  workflowId?: string;
  parameterMapping?: {
    [key: string]: string;
  };
}

export interface EdgeData {
  conditionExpression?: string;
}

export type WorkflowNode = Node<NodeData>;

export type WorkflowEdge = Edge<EdgeData> & {
  type: EdgeType;
  markerEnd?: EdgeMarker;
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

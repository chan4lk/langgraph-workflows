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

interface NodeData {
  label: string;
  // Agent node specific data
  agentName?: string;
  description?: string;
  llmConfigId?: string;
  promptTemplateId?: string;
  tools?: string[];
  // Function node specific data
  functionName?: string;
  // Human task node specific data
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
  // Sub-workflow node specific data
  workflowId?: string;
  parameterMapping?: {
    [key: string]: string;
  };
}

interface EdgeData {
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

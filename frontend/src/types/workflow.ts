import { Node, Edge } from 'reactflow';

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

export interface WorkflowNode extends Node {
  id: string;
  type: NodeType;
  position: { x: number; y: number };
  data: {
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
  };
  draggable?: boolean;
  selectable?: boolean;
}

export interface WorkflowEdge extends Edge {
  id: string;
  source: string;
  target: string;
  type: EdgeType;
  data?: {
    conditionExpression?: string;
  };
}

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

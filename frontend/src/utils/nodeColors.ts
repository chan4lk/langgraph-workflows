import { NodeType } from '../types/workflow';

const nodeColors: Record<NodeType, string> = {
  start: '#4caf50',
  end: '#f44336',
  agent: '#2196f3',
  function: '#9c27b0',
  human_task: '#00bcd4',
  sub_workflow: '#ff9800',
  tool: '#8bc34a',
  fork: '#795548',
  join: '#607d8b',
};

export const getNodeColor = (type: NodeType): string => nodeColors[type] || '#555';

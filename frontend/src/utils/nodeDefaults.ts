import { NodeData } from '../types/workflow';

export const getDefaultNodeData = (): NodeData => ({
  label: '',
  description: '',
  agentName: '',
  llmConfigId: '',
  promptTemplateId: '',
  template: null,
  tools: [],
  functionName: '',
  taskName: '',
  assignmentRules: { users: [], groups: [] },
  inputFields: [],
  workflowId: '',
  parameterMapping: {}
});

export const getAgentNodeData = (): NodeData => ({
  ...getDefaultNodeData(),
  label: 'Agent',
  agentName: 'New Agent',
  description: 'A new agent node',
  llmConfigId: 'gpt-4',
  promptTemplateId: '',
  template: null,
  tools: []
});

export const getHumanTaskNodeData = (): NodeData => ({
  ...getDefaultNodeData(),
  label: 'Human Task',
  taskName: 'New Task',
  description: 'A new human task',
  assignmentRules: { users: [], groups: [] }
});

export const getSubWorkflowNodeData = (): NodeData => ({
  ...getDefaultNodeData(),
  label: 'Sub Workflow',
  description: 'A new sub-workflow',
  workflowId: ''
});

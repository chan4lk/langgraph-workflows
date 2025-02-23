import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class AgentNodeCreator extends BaseNodeCreator {
  protected type: NodeType = NodeType.AGENT;

  getDefaultData(): NodeData {
    return {
      label: 'Agent',
      type: this.type,
      description: 'A new agent node',
      agentName: 'New Agent',
      llmConfigId: 'gpt-4',
      promptTemplateId: '',
      template: null,
      tools: [],
      functionName: '',
      taskName: '',
      assignmentRules: { users: [], groups: [] },
      inputFields: [],
      workflowId: '',
      parameterMapping: {},
    };
  }

  validateData(data: NodeData): boolean {
    return !!(data.agentName && data.llmConfigId);
  }
}

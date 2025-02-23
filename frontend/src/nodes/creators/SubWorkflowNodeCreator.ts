import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class SubWorkflowNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'sub_workflow';

  getDefaultData(): NodeData {
    return {
      label: 'Sub-workflow',
      description: 'A new sub-workflow',
      workflowId: '',
      parameterMapping: {},
    };
  }

  validateData(data: NodeData): boolean {
    return !!data.workflowId;
  }
}

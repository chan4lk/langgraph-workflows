import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class EndNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'end';

  getDefaultData(): NodeData {
    return {
      label: 'End',
      description: 'End point of the workflow',
      type: this.type,
    };
  }

  validateData(data: NodeData): boolean {
    return data.type === this.type && !!data.label;
  }
}

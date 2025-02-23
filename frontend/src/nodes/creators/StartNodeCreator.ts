import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class StartNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'start';

  getDefaultData(): NodeData {
    return {
      label: 'Start',
      description: 'Starting point of the workflow',
      type: this.type,
    };
  }

  validateData(data: NodeData): boolean {
    return data.type === this.type && !!data.label;
  }
}

import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class FunctionNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'function';

  getDefaultData(): NodeData {
    return {
      label: 'Function',
      description: 'A new function node',
      functionName: 'New Function',
    };
  }

  validateData(data: NodeData): boolean {
    return !!data.functionName;
  }
}

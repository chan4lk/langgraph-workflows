import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class JoinNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'join';

  getDefaultData(): NodeData {
    return {
      label: 'Join',
      description: 'Merge parallel branches back into single flow',
      type: this.type,
      joinType: 'all', // Default to waiting for all branches
    };
  }

  validateData(data: NodeData): boolean {
    return data.type === this.type && 
           !!data.label && 
           (data.joinType === 'all' || data.joinType === 'any');
  }

  updateData(data: NodeData, updates: Partial<NodeData>): NodeData {
    const updatedData = super.updateData(data, updates);
    // Ensure joinType is valid
    if (updatedData.joinType !== 'all' && updatedData.joinType !== 'any') {
      updatedData.joinType = 'all';
    }
    return updatedData;
  }
}

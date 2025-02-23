import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class ForkNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'fork';

  getDefaultData(): NodeData {
    return {
      label: 'Fork',
      description: 'Split workflow into parallel branches',
      type: this.type,
      branches: [], // Initialize with empty array
    };
  }

  validateData(data: NodeData): boolean {
    return data.type === this.type && 
           !!data.label && 
           Array.isArray(data.branches);
  }

  updateData(data: NodeData, updates: Partial<NodeData>): NodeData {
    const updatedData = super.updateData(data, updates);
    // Ensure branches is always an array
    if (!Array.isArray(updatedData.branches)) {
      updatedData.branches = [];
    }
    return updatedData;
  }
}

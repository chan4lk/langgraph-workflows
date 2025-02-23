import { XYPosition } from 'reactflow';
import { WorkflowNode, NodeData, NodeType } from '../../types/workflow';
import { NodeCreator } from '../NodeFactory';

export abstract class BaseNodeCreator implements NodeCreator {
  protected abstract type: NodeType;

  createNode(position: XYPosition): WorkflowNode {
    return {
      id: `${this.type}-${Date.now()}`,
      type: this.type,
      position,
      draggable: true,
      data: {
        ...this.getDefaultData(),
        type: this.type // Always include type in node data
      },
    };
  }

  abstract getDefaultData(): NodeData;

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  validateData(_: NodeData): boolean {
    return true;
  }

  updateData(data: NodeData, updates: Partial<NodeData>): NodeData {
    return { 
      ...data, 
      ...updates,
      type: this.type // Ensure type is preserved during updates
    };
  }
}

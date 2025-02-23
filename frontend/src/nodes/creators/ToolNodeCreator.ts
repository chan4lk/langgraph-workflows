import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType, WorkflowNode } from '../../types/workflow';
import { ToolConfig } from '../../types/tool';
import { XYPosition } from 'reactflow';

export class ToolNodeCreator extends BaseNodeCreator {
  protected type: NodeType = NodeType.TOOL;

  createNode(position: XYPosition): WorkflowNode {
    return {
      id: crypto.randomUUID(),
      type: this.type,
      position,
      draggable: true,
      data: this.getDefaultData(),
    };
  }

  getDefaultData(): NodeData {
    return {
      type: NodeType.TOOL,
      label: 'Tool',
      description: '',
      tools: [],
      toolId: '',
      toolConfig: undefined,
    };
  }

  validateData(data: NodeData): boolean {
    if (!data.toolId) return false;
    if (!data.toolConfig) return false;
    
    const config = data.toolConfig as ToolConfig;
    if (config.type === 'api') {
      return !!config.api_config;
    }
    if (config.type === 'code_block') {
      return !!config.code_block_config;
    }
    return false;
  }

  updateData(data: NodeData, updates: Partial<NodeData>): NodeData {
    const updatedData = super.updateData(data, updates);
    if (updates.toolConfig) {
      // Ensure toolConfig is properly typed
      updatedData.toolConfig = updates.toolConfig as ToolConfig;
    }
    return updatedData;
  }
}

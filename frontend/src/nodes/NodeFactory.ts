import { XYPosition } from 'reactflow';
import { NodeType, WorkflowNode, NodeData } from '../types/workflow';
import { nodeCreators } from './creators';

export interface NodeCreator {
  createNode(position: XYPosition): WorkflowNode;
  getDefaultData(): NodeData;
  validateData?(data: NodeData): boolean;
  updateData?(data: NodeData, updates: Partial<NodeData>): NodeData;
}

export class NodeFactory {
  private static instance: NodeFactory;
  private creators: Map<NodeType, NodeCreator>;

  private constructor() {
    this.creators = new Map(Object.entries(nodeCreators) as [NodeType, NodeCreator][]);
  }

  public static getInstance(): NodeFactory {
    if (!NodeFactory.instance) {
      NodeFactory.instance = new NodeFactory();
    }
    return NodeFactory.instance;
  }

  public createNode(type: NodeType, position: XYPosition): WorkflowNode {
    const creator = this.creators.get(type);
    if (!creator) {
      throw new Error(`No creator found for node type: ${type}`);
    }
    return creator.createNode(position);
  }

  public getDefaultData(type: NodeType): NodeData {
    const creator = this.creators.get(type);
    if (!creator) {
      throw new Error(`No creator found for node type: ${type}`);
    }
    return creator.getDefaultData();
  }

  public validateData(type: NodeType, data: NodeData): boolean {
    const creator = this.creators.get(type);
    if (!creator) {
      throw new Error(`No creator found for node type: ${type}`);
    }
    return creator.validateData ? creator.validateData(data) : true;
  }

  public updateData(type: NodeType, data: NodeData, updates: Partial<NodeData>): NodeData {
    const creator = this.creators.get(type);
    if (!creator) {
      throw new Error(`No creator found for node type: ${type}`);
    }
    return creator.updateData ? creator.updateData(data, updates) : { ...data, ...updates };
  }

  public getAvailableNodeTypes(): NodeType[] {
    return Array.from(this.creators.keys());
  }
}

import { NodeType, WorkflowNode, NodeData } from '../types/workflow';
import { XYPosition } from 'reactflow';
import { 
  AgentNodeCreator,
  HumanTaskNodeCreator,
  SubWorkflowNodeCreator,
  FunctionNodeCreator,
  StartNodeCreator,
  EndNodeCreator,
  ForkNodeCreator,
  JoinNodeCreator,
} from './creators';

export interface NodeCreator {
  createNode(position: XYPosition): WorkflowNode;
  getDefaultData(): NodeData;
  validateData?(data: NodeData): boolean;
  updateData?(data: NodeData, updates: Partial<NodeData>): NodeData;
}

export class NodeFactory {
  private static readonly creators: ReadonlyMap<NodeType, NodeCreator> = new Map<NodeType, NodeCreator>([
    ['agent', new AgentNodeCreator()],
    ['human_task', new HumanTaskNodeCreator()],
    ['sub_workflow', new SubWorkflowNodeCreator()],
    ['function', new FunctionNodeCreator()],
    ['start', StartNodeCreator],
    ['end', EndNodeCreator],
    ['fork', ForkNodeCreator],
    ['join', JoinNodeCreator],
  ]);

  static createNode(type: NodeType, position: XYPosition): WorkflowNode {
    const creator = this.creators.get(type);
    if (!creator) {
      throw new Error(`No creator found for node type: ${type}`);
    }
    return creator.createNode(position);
  }

  static getDefaultData(type: NodeType): NodeData {
    const creator = this.creators.get(type);
    if (!creator) {
      throw new Error(`No creator found for node type: ${type}`);
    }
    return creator.getDefaultData();
  }

  static validateData(type: NodeType, data: NodeData): boolean {
    const creator = this.creators.get(type);
    if (!creator || !creator.validateData) {
      return true;
    }
    return creator.validateData(data);
  }

  static updateData(type: NodeType, data: NodeData, updates: Partial<NodeData>): NodeData {
    const creator = this.creators.get(type);
    if (!creator || !creator.updateData) {
      return { ...data, ...updates };
    }
    return creator.updateData(data, updates);
  }
}

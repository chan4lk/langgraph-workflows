import { BaseNodeCreator } from './BaseNodeCreator';
import { AgentNodeCreator } from './AgentNodeCreator';
import { FunctionNodeCreator } from './FunctionNodeCreator';
import { ToolNodeCreator } from './ToolNodeCreator';
import { HumanTaskNodeCreator } from './HumanTaskNodeCreator';
import { SubWorkflowNodeCreator } from './SubWorkflowNodeCreator';
import { NodeType, NodeData } from '../../types/workflow';

class SimpleNodeCreator extends BaseNodeCreator {
  protected type: NodeType;

  constructor(type: NodeType) {
    super();
    this.type = type;
  }

  getDefaultData(): NodeData {
    return {
      label: this.type.charAt(0).toUpperCase() + this.type.slice(1),
      type: this.type,
    };
  }
}

export const nodeCreators = {
  [NodeType.START]: new SimpleNodeCreator(NodeType.START),
  [NodeType.END]: new SimpleNodeCreator(NodeType.END),
  [NodeType.AGENT]: new AgentNodeCreator(),
  [NodeType.FUNCTION]: new FunctionNodeCreator(),
  [NodeType.TOOL]: new ToolNodeCreator(),
  [NodeType.HUMAN_TASK]: new HumanTaskNodeCreator(),
  [NodeType.SUB_WORKFLOW]: new SubWorkflowNodeCreator(),
  [NodeType.FORK]: new SimpleNodeCreator(NodeType.FORK),
  [NodeType.JOIN]: new SimpleNodeCreator(NodeType.JOIN),
};

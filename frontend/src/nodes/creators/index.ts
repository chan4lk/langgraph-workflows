export * from './AgentNodeCreator';
export * from './HumanTaskNodeCreator';
export * from './SubWorkflowNodeCreator';
export * from './FunctionNodeCreator';

import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeType } from '../../types/workflow';

class SimpleNodeCreator extends BaseNodeCreator {
  constructor(protected type: NodeType) {
    super();
  }

  getDefaultData() {
    return {
      label: this.type.charAt(0).toUpperCase() + this.type.slice(1).replace('_', ' '),
    };
  }
}

export const StartNodeCreator = new SimpleNodeCreator('start');
export const EndNodeCreator = new SimpleNodeCreator('end');
export const ForkNodeCreator = new SimpleNodeCreator('fork');
export const JoinNodeCreator = new SimpleNodeCreator('join');

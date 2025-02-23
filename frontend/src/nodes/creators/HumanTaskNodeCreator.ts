import { BaseNodeCreator } from './BaseNodeCreator';
import { NodeData, NodeType } from '../../types/workflow';

export class HumanTaskNodeCreator extends BaseNodeCreator {
  protected type: NodeType = 'human_task';

  getDefaultData(): NodeData {
    return {
      label: 'Human Task',
      description: 'A new human task',
      taskName: 'New Task',
      assignmentRules: {
        users: [],
        groups: [],
      },
      inputFields: [],
    };
  }

  validateData(data: NodeData): boolean {
    return !!(data.taskName && data.assignmentRules);
  }
}

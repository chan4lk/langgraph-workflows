import { BaseNode } from '../components/nodes/BaseNode';
import { AgentNode } from '../components/nodes/AgentNode';
import { HumanTaskNode } from '../components/nodes/HumanTaskNode';
import { SubWorkflowNode } from '../components/nodes/SubWorkflowNode';
import { ToolNode } from '../components/nodes/ToolNode';

export const nodeTypes = {
  base: BaseNode,
  start: BaseNode,
  end: BaseNode,
  agent: AgentNode,
  function: BaseNode,
  human_task: HumanTaskNode,
  sub_workflow: SubWorkflowNode,
  tool: ToolNode,
};

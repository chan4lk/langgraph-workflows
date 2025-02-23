import { 
  Paper, 
  List, 
  ListItem, 
  ListItemButton,
  ListItemIcon,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  SmartToy,
  Functions,
  Person,
  PlayArrow,
  Stop,
  Build,
  AccountTree,
  CallSplit,
  CallMerge,
  SvgIconComponent,
} from '@mui/icons-material';
import { useWorkflowStore } from '../store/workflowStore';
import { NodeType } from '../types/workflow';
import { NodeFactory } from '../nodes/NodeFactory';

const nodeIcons: Record<NodeType, SvgIconComponent> = {
  [NodeType.AGENT]: SmartToy,
  [NodeType.FUNCTION]: Functions,
  [NodeType.HUMAN_TASK]: Person,
  [NodeType.START]: PlayArrow,
  [NodeType.END]: Stop,
  [NodeType.TOOL]: Build,
  [NodeType.SUB_WORKFLOW]: AccountTree,
  [NodeType.FORK]: CallSplit,
  [NodeType.JOIN]: CallMerge,
};

const getNextNodePosition = (nodes: any[]) => {
  const maxY = nodes.reduce((max, node) => Math.max(max, node.position.y), 0);
  return { x: 250, y: maxY + 100 };
};

export const Toolbar = () => {
  const nodes = useWorkflowStore((state) => state.currentWorkflow?.nodes || []);
  const addNode = useWorkflowStore((state) => state.addNode);
  const nodeFactory = NodeFactory.getInstance();
  const availableNodeTypes = nodeFactory.getAvailableNodeTypes();

  const handleAddNode = (type: NodeType) => {
    const position = getNextNodePosition(nodes);
    const node = nodeFactory.createNode(type, position);
    addNode(node);
  };

  return (
    <Paper
      elevation={2}
      sx={{
        position: 'fixed',
        left: 16,
        top: 16,
        zIndex: 1000,
        bgcolor: 'background.paper',
        borderRadius: 1,
      }}
    >
      <List>
        {availableNodeTypes.map((type) => {
          const Icon = nodeIcons[type];
          return Icon ? (
            <ListItem key={type} disablePadding>
              <Tooltip title={type} placement="right">
                <ListItemButton onClick={() => handleAddNode(type)}>
                  <ListItemIcon>
                    <Icon />
                  </ListItemIcon>
                </ListItemButton>
              </Tooltip>
            </ListItem>
          ) : null;
        })}
        <Divider />
      </List>
    </Paper>
  );
};

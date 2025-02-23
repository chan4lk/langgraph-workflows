import { 
  Paper, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemButton,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  SmartToy,
  Person,
  Functions,
  PlayArrow,
  Stop,
  AccountTree
} from '@mui/icons-material';
import { useWorkflowStore } from '../store/workflowStore';
import { NodeType, WorkflowNode } from '../types/workflow';
import { NodeFactory } from '../nodes/NodeFactory';

interface Position {
  x: number;
  y: number;
}

const getNextNodePosition = (nodes: WorkflowNode[]): Position => {
  if (nodes.length === 0) {
    return { x: 250, y: 100 };
  }
  const maxY = Math.max(...nodes.map(node => node.position.y));
  return { x: 250, y: maxY + 100 };
};

export const Toolbar = () => {
  const nodes = useWorkflowStore((state) => state.currentWorkflow?.nodes || []);
  const addNode = useWorkflowStore((state) => state.addNode);

  const handleAddNode = (type: NodeType) => {
    const position = getNextNodePosition(nodes);
    const node = NodeFactory.createNode(type, position);
    addNode(node);
  };

  return (
    <Paper
      elevation={3}
      sx={{
        position: 'fixed',
        left: 20,
        top: 80,
        width: 'auto',
        zIndex: 1000,
        borderRadius: 2,
      }}
    >
      <List>
        <ListItem disablePadding>
          <Tooltip title="Add Agent" placement="right">
            <ListItemButton onClick={() => handleAddNode('agent')}>
              <ListItemIcon>
                <SmartToy />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
        <ListItem disablePadding>
          <Tooltip title="Add Human Task" placement="right">
            <ListItemButton onClick={() => handleAddNode('human_task')}>
              <ListItemIcon>
                <Person />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
        <ListItem disablePadding>
          <Tooltip title="Add Function" placement="right">
            <ListItemButton onClick={() => handleAddNode('function')}>
              <ListItemIcon>
                <Functions />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
        <ListItem disablePadding>
          <Tooltip title="Add Sub-workflow" placement="right">
            <ListItemButton onClick={() => handleAddNode('sub_workflow')}>
              <ListItemIcon>
                <AccountTree />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
        <Divider />
        <ListItem disablePadding>
          <Tooltip title="Add Start" placement="right">
            <ListItemButton onClick={() => handleAddNode('start')}>
              <ListItemIcon>
                <PlayArrow />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
        <ListItem disablePadding>
          <Tooltip title="Add End" placement="right">
            <ListItemButton onClick={() => handleAddNode('end')}>
              <ListItemIcon>
                <Stop />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
      </List>
    </Paper>
  );
};

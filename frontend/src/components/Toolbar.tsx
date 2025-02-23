import React from 'react';
import { 
  Paper, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemButton,
  Tooltip,
  Divider,
  Box,
  Typography
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  SmartToy,
  Functions,
  Person,
  AccountTree
} from '@mui/icons-material';
import { useWorkflowStore } from '../store/workflowStore';
import { NodeType, WorkflowNode } from '../types/workflow';
import { 
  getDefaultNodeData, 
  getAgentNodeData, 
  getHumanTaskNodeData, 
  getSubWorkflowNodeData 
} from '../utils/nodeDefaults';

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

export const Toolbar: React.FC = () => {
  const { addNode, currentWorkflow } = useWorkflowStore();

  const handleAddNode = (type: NodeType) => {
    const position = getNextNodePosition(currentWorkflow?.nodes || []);
    
    const nodeData = {
      id: `${type}-${Date.now()}`,
      type,
      position,
      draggable: true,
      data: getDefaultNodeData()
    };

    switch (type) {
      case 'agent':
        nodeData.data = getAgentNodeData();
        break;
      case 'human_task':
        nodeData.data = getHumanTaskNodeData();
        break;
      case 'sub_workflow':
        nodeData.data = getSubWorkflowNodeData();
        break;
      default:
        nodeData.data.label = type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ');
    }

    addNode(nodeData);
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
        bgcolor: 'background.paper',
      }}
    >
      <Box sx={{ p: 1 }}>
        <Typography variant="subtitle2" sx={{ px: 1, color: 'text.secondary' }}>
          Add Nodes
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem disablePadding>
          <Tooltip title="Start Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('start')}>
              <ListItemIcon>
                <PlayArrow color="success" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="End Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('end')}>
              <ListItemIcon>
                <Stop color="error" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <Divider />

        <ListItem disablePadding>
          <Tooltip title="Agent Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('agent')}>
              <ListItemIcon>
                <SmartToy />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="Function Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('function')}>
              <ListItemIcon>
                <Functions />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="Human Task Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('human_task')}>
              <ListItemIcon>
                <Person />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="Sub-workflow Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('sub_workflow')}>
              <ListItemIcon>
                <AccountTree />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
      </List>
    </Paper>
  );
};

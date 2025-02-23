import React from 'react';
import { 
  Paper, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  ListItemButton,
  Tooltip,
  Divider
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
import { NodeType } from '../types/workflow';

const getNextNodePosition = (nodes: any[]) => {
  if (nodes.length === 0) {
    return { x: 250, y: 100 };
  }

  // Find the lowest y-position
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
      data: {
        label: type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' '),
      },
    };

    switch (type) {
      case 'agent':
        nodeData.data = {
          ...nodeData.data,
          agentName: 'New Agent',
          description: 'A new agent node',
        };
        break;
      case 'human_task':
        nodeData.data = {
          ...nodeData.data,
          taskName: 'New Task',
          description: 'A new human task',
          assignmentRules: {
            users: [],
            groups: [],
          },
        };
        break;
      case 'sub_workflow':
        nodeData.data = {
          ...nodeData.data,
          workflowId: '',
          description: 'A new sub-workflow',
        };
        break;
    }

    addNode(nodeData);
  };

  return (
    <Paper
      elevation={3}
      sx={{
        position: 'fixed',
        left: 20,
        top: 20,
        width: 'auto',
        zIndex: 1000,
      }}
    >
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
          <Tooltip title="Agent Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('agent')}>
              <ListItemIcon>
                <SmartToy color="primary" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="Function Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('function')}>
              <ListItemIcon>
                <Functions color="secondary" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="Human Task" placement="right">
            <ListItemButton onClick={() => handleAddNode('human_task')}>
              <ListItemIcon>
                <Person color="info" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <ListItem disablePadding>
          <Tooltip title="Sub-workflow" placement="right">
            <ListItemButton onClick={() => handleAddNode('sub_workflow')}>
              <ListItemIcon>
                <AccountTree color="warning" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>

        <Divider />

        <ListItem disablePadding>
          <Tooltip title="End Node" placement="right">
            <ListItemButton onClick={() => handleAddNode('end')}>
              <ListItemIcon>
                <Stop color="error" />
              </ListItemIcon>
            </ListItemButton>
          </Tooltip>
        </ListItem>
      </List>
    </Paper>
  );
};

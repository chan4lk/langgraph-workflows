import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Paper, Typography, Box } from '@mui/material';
import { WorkflowNode } from '../../types/workflow';
import { useWorkflowStore } from '../../store/workflowStore';

interface BaseNodeProps extends NodeProps {
  data: WorkflowNode['data'];
  children?: React.ReactNode;
}

export const BaseNode: React.FC<BaseNodeProps> = ({ 
  id, 
  data, 
  selected,
  type,
  children 
}) => {
  const setSelectedNode = useWorkflowStore((state) => state.setSelectedNode);

  const handleClick = () => {
    setSelectedNode({ id, data, position: { x: 0, y: 0 }, type });
  };

  const getNodeColor = () => {
    switch (type) {
      case 'start':
        return '#4caf50';
      case 'end':
        return '#f44336';
      case 'agent':
        return '#2196f3';
      case 'function':
        return '#9c27b0';
      case 'human_task':
        return '#00bcd4';
      case 'sub_workflow':
        return '#ff9800';
      default:
        return '#555';
    }
  };

  return (
    <Paper
      elevation={selected ? 8 : 2}
      onClick={handleClick}
      sx={{
        padding: 2,
        minWidth: 180,
        backgroundColor: selected ? `${getNodeColor()}22` : 'white',
        border: `2px solid ${selected ? getNodeColor() : '#ccc'}`,
        borderRadius: 2,
        cursor: 'pointer',
      }}
    >
      {type !== 'start' && (
        <Handle
          type="target"
          position={Position.Top}
          style={{ background: getNodeColor() }}
        />
      )}
      
      <Box>
        <Typography 
          variant="subtitle1" 
          fontWeight="bold"
          sx={{ color: getNodeColor() }}
        >
          {data.label}
        </Typography>
        {data.description && (
          <Typography variant="body2" color="text.secondary">
            {data.description}
          </Typography>
        )}
        {children}
      </Box>

      {type !== 'end' && (
        <Handle
          type="source"
          position={Position.Bottom}
          style={{ background: getNodeColor() }}
        />
      )}
    </Paper>
  );
};

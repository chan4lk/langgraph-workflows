import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Paper, Typography, Box } from '@mui/material';
import { WorkflowNode } from '../../types/workflow';
import { useWorkflowStore } from '../../store/workflowStore';

interface BaseNodeProps extends NodeProps {
  data: WorkflowNode['data'];
}

export const BaseNode: React.FC<BaseNodeProps> = ({ 
  id, 
  data, 
  selected 
}) => {
  const setSelectedNode = useWorkflowStore((state) => state.setSelectedNode);

  const handleClick = () => {
    setSelectedNode({ id, data, position: { x: 0, y: 0 }, type: 'agent' });
  };

  return (
    <Paper
      elevation={selected ? 8 : 2}
      onClick={handleClick}
      sx={{
        padding: 2,
        minWidth: 180,
        backgroundColor: selected ? '#e3f2fd' : 'white',
        border: selected ? '2px solid #2196f3' : '1px solid #ccc',
        borderRadius: 2,
        cursor: 'pointer',
      }}
    >
      <Handle
        type="target"
        position={Position.Top}
        style={{ background: '#555' }}
      />
      
      <Box>
        <Typography variant="subtitle1" fontWeight="bold">
          {data.label}
        </Typography>
        {data.description && (
          <Typography variant="body2" color="text.secondary">
            {data.description}
          </Typography>
        )}
      </Box>

      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: '#555' }}
      />
    </Paper>
  );
};

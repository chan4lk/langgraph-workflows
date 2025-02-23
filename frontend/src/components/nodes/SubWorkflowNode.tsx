import React from 'react';
import { NodeProps } from 'reactflow';
import { AccountTree } from '@mui/icons-material';
import { Box } from '@mui/material';
import { BaseNode } from './BaseNode';
import { WorkflowNode } from '../../types/workflow';

interface SubWorkflowNodeProps extends NodeProps {
  data: WorkflowNode['data'];
}

export const SubWorkflowNode: React.FC<SubWorkflowNodeProps> = (props) => {
  return (
    <BaseNode {...props}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
        <AccountTree color="primary" />
        <Box>
          {props.data.workflowId && (
            <div>Workflow: {props.data.workflowId}</div>
          )}
        </Box>
      </Box>
    </BaseNode>
  );
};

import React from 'react';
import { NodeProps } from 'reactflow';
import { Person } from '@mui/icons-material';
import { Box } from '@mui/material';
import { BaseNode } from './BaseNode';
import { WorkflowNode } from '../../types/workflow';

interface HumanTaskNodeProps extends NodeProps {
  data: WorkflowNode['data'];
}

export const HumanTaskNode: React.FC<HumanTaskNodeProps> = (props) => {
  return (
    <BaseNode {...props}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
        <Person color="primary" />
        <Box>
          {props.data.taskName && (
            <div>Task: {props.data.taskName}</div>
          )}
          {props.data.assignmentRules?.users && (
            <div>Assignees: {props.data.assignmentRules.users.join(', ')}</div>
          )}
        </Box>
      </Box>
    </BaseNode>
  );
};

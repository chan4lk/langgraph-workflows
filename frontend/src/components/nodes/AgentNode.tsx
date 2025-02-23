import React from 'react';
import { NodeProps } from 'reactflow';
import { SmartToy } from '@mui/icons-material';
import { Box } from '@mui/material';
import { BaseNode } from './BaseNode';
import { WorkflowNode } from '../../types/workflow';

interface AgentNodeProps extends NodeProps {
  data: WorkflowNode['data'];
}

export const AgentNode: React.FC<AgentNodeProps> = (props) => {
  return (
    <BaseNode {...props}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
        <SmartToy color="primary" />
        <Box>
          {props.data.agentName && (
            <div>Agent: {props.data.agentName}</div>
          )}
          {props.data.llmConfigId && (
            <div>LLM: {props.data.llmConfigId}</div>
          )}
        </Box>
      </Box>
    </BaseNode>
  );
};

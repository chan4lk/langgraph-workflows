import React from 'react';
import { Box } from '@mui/material';
import { ReactFlowProvider } from 'reactflow';
import { WorkflowDesigner } from './WorkflowDesigner';
import { WorkflowToolbar } from './toolbar/WorkflowToolbar';

export const WorkflowLayout: React.FC = () => {
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <WorkflowToolbar />
      <Box sx={{ flexGrow: 1, position: 'relative' }}>
        <ReactFlowProvider>
          <WorkflowDesigner />
        </ReactFlowProvider>
      </Box>
    </Box>
  );
};

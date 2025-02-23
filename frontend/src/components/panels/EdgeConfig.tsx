import React from 'react';
import { Stack, TextField } from '@mui/material';
import { EdgeData } from '../../types/workflow';
import { WorkflowEdge } from '../../types/workflow';

interface EdgeConfigProps {
  edge: WorkflowEdge;
  onEdgeUpdate: (field: keyof EdgeData, value: any) => void;
}

export const EdgeConfig: React.FC<EdgeConfigProps> = ({
  edge,
  onEdgeUpdate,
}) => {
  const data = edge.data || {};

  return (
    <Stack spacing={2}>
      <TextField
        fullWidth
        label="Label"
        value={data.label || ''}
        onChange={(e) => onEdgeUpdate('label', e.target.value)}
      />
      <TextField
        fullWidth
        label="Condition"
        multiline
        rows={2}
        value={data.condition || ''}
        onChange={(e) => onEdgeUpdate('condition', e.target.value)}
      />
    </Stack>
  );
};

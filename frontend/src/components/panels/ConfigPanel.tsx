import React, { useEffect } from 'react';
import {
  Paper,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Stack,
} from '@mui/material';
import { useWorkflowStore } from '../../store/workflowStore';
import { NodeType, EdgeType } from '../../types/workflow';

export const ConfigPanel: React.FC = () => {
  const selectedNode = useWorkflowStore((state) => state.selectedNode);
  const selectedEdge = useWorkflowStore((state) => state.selectedEdge);
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const updateEdge = useWorkflowStore((state) => state.updateEdge);

  useEffect(() => {
    console.log('ConfigPanel re-render with:', { selectedNode, selectedEdge });
  }, [selectedNode, selectedEdge]);

  const renderNodeConfig = () => {
    console.log(selectedNode);
    if (!selectedNode) return null;

    const handleNodeUpdate = (field: string, value: unknown) => {
      updateNode(selectedNode.id, {
        data: { ...selectedNode.data, [field]: value }
      });
    };

    const commonFields = (
      <Stack spacing={2}>
        <TextField
          fullWidth
          label="Label"
          value={selectedNode.data?.label || ''}
          onChange={(e) => handleNodeUpdate('label', e.target.value)}
          size="small"
        />
        <TextField
          fullWidth
          label="Description"
          value={selectedNode.data?.description || ''}
          onChange={(e) => handleNodeUpdate('description', e.target.value)}
          multiline
          rows={2}
          size="small"
        />
      </Stack>
    );

    const renderSpecificFields = () => {
      switch (selectedNode.type as NodeType) {
        case 'agent':
          return (
            <Stack spacing={2}>
              <TextField
                fullWidth
                label="Agent Name"
                value={selectedNode.data?.agentName || ''}
                onChange={(e) => handleNodeUpdate('agentName', e.target.value)}
                size="small"
              />
              <FormControl fullWidth size="small">
                <InputLabel>LLM Configuration</InputLabel>
                <Select
                  value={selectedNode.data?.llmConfigId || ''}
                  onChange={(e) => handleNodeUpdate('llmConfigId', e.target.value)}
                  label="LLM Configuration"
                >
                  <MenuItem value="gpt-4">GPT-4</MenuItem>
                  <MenuItem value="gpt-3.5-turbo">GPT-3.5 Turbo</MenuItem>
                </Select>
              </FormControl>
            </Stack>
          );

        case 'human_task':
          return (
            <Stack spacing={2}>
              <TextField
                fullWidth
                label="Task Name"
                value={selectedNode.data?.taskName || ''}
                onChange={(e) => handleNodeUpdate('taskName', e.target.value)}
                size="small"
              />
              <TextField
                fullWidth
                label="Assignee"
                value={selectedNode.data?.assignmentRules?.users?.[0] || ''}
                onChange={(e) => handleNodeUpdate('assignmentRules', { users: [e.target.value] })}
                size="small"
              />
            </Stack>
          );

        case 'sub_workflow':
          return (
            <Stack spacing={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Workflow</InputLabel>
                <Select
                  value={selectedNode.data?.workflowId || ''}
                  onChange={(e) => handleNodeUpdate('workflowId', e.target.value)}
                  label="Workflow"
                >
                  <MenuItem value="workflow1">Workflow 1</MenuItem>
                  <MenuItem value="workflow2">Workflow 2</MenuItem>
                </Select>
              </FormControl>
            </Stack>
          );

        case 'start':
        case 'end':
        case 'function':
        default:
          return null;
      }
    };

    return (
      <Stack spacing={2}>
        <Typography variant="h6" gutterBottom>
          Node Configuration
        </Typography>
        {commonFields}
        {renderSpecificFields()}
      </Stack>
    );
  };

  const renderEdgeConfig = () => {
    if (!selectedEdge) return null;

    return (
      <Stack spacing={2}>
        <Typography variant="h6">Edge Configuration</Typography>
        <FormControl fullWidth>
          <InputLabel>Edge Type</InputLabel>
          <Select
            value={selectedEdge.type}
            onChange={(e) => updateEdge(selectedEdge.id, { type: e.target.value as EdgeType })}
            label="Edge Type"
          >
            <MenuItem value="default">Default</MenuItem>
            <MenuItem value="success">Success</MenuItem>
            <MenuItem value="failure">Failure</MenuItem>
          </Select>
        </FormControl>
      </Stack>
    );
  };

  if (!selectedNode && !selectedEdge) {
    return null;
  }

  return (
    <Paper
      elevation={3}
      sx={{
        position: 'fixed',
        right: 20,
        top: 20,
        width: 300,
        padding: 3,
        maxHeight: 'calc(100vh - 40px)',
        overflowY: 'auto',
        zIndex: 9999,
        backgroundColor: 'background.paper',
        borderRadius: 2,
      }}
    >
      <Stack spacing={3}>
        {selectedNode && renderNodeConfig()}
        {selectedEdge && renderEdgeConfig()}
      </Stack>
    </Paper>
  );
};

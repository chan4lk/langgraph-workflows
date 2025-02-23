import React from 'react';
import {
  Paper,
  Typography,
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
} from '@mui/material';
import { useWorkflowStore } from '../../store/workflowStore';
import { NodeType } from '../../types/workflow';

export const ConfigPanel: React.FC = () => {
  const selectedNode = useWorkflowStore((state) => state.selectedNode);
  const selectedEdge = useWorkflowStore((state) => state.selectedEdge);
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const updateEdge = useWorkflowStore((state) => state.updateEdge);

  if (!selectedNode && !selectedEdge) {
    return null;
  }

  const renderNodeConfig = () => {
    if (!selectedNode) return null;

    const handleNodeUpdate = (field: string, value: any) => {
      updateNode(selectedNode.id, {
        data: { ...selectedNode.data, [field]: value }
      });
    };

    const commonFields = (
      <>
        <TextField
          fullWidth
          label="Label"
          value={selectedNode.data.label || ''}
          onChange={(e) => handleNodeUpdate('label', e.target.value)}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Description"
          value={selectedNode.data.description || ''}
          onChange={(e) => handleNodeUpdate('description', e.target.value)}
          margin="normal"
          multiline
          rows={2}
        />
      </>
    );

    const renderSpecificFields = () => {
      switch (selectedNode.type as NodeType) {
        case 'agent':
          return (
            <>
              <TextField
                fullWidth
                label="Agent Name"
                value={selectedNode.data.agentName || ''}
                onChange={(e) => handleNodeUpdate('agentName', e.target.value)}
                margin="normal"
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>LLM Configuration</InputLabel>
                <Select
                  value={selectedNode.data.llmConfigId || ''}
                  onChange={(e) => handleNodeUpdate('llmConfigId', e.target.value)}
                  label="LLM Configuration"
                >
                  <MenuItem value="gpt-4">GPT-4</MenuItem>
                  <MenuItem value="gpt-3.5-turbo">GPT-3.5 Turbo</MenuItem>
                </Select>
              </FormControl>
            </>
          );

        case 'human_task':
          return (
            <>
              <TextField
                fullWidth
                label="Task Name"
                value={selectedNode.data.taskName || ''}
                onChange={(e) => handleNodeUpdate('taskName', e.target.value)}
                margin="normal"
              />
              {/* Add more human task specific fields */}
            </>
          );

        case 'sub_workflow':
          return (
            <>
              <FormControl fullWidth margin="normal">
                <InputLabel>Workflow</InputLabel>
                <Select
                  value={selectedNode.data.workflowId || ''}
                  onChange={(e) => handleNodeUpdate('workflowId', e.target.value)}
                  label="Workflow"
                >
                  <MenuItem value="workflow1">Workflow 1</MenuItem>
                  <MenuItem value="workflow2">Workflow 2</MenuItem>
                </Select>
              </FormControl>
              {/* Add parameter mapping fields */}
            </>
          );

        default:
          return null;
      }
    };

    return (
      <>
        <Typography variant="h6" gutterBottom>
          Node Configuration
        </Typography>
        {commonFields}
        {renderSpecificFields()}
      </>
    );
  };

  const renderEdgeConfig = () => {
    if (!selectedEdge) return null;

    return (
      <>
        <Typography variant="h6" gutterBottom>
          Edge Configuration
        </Typography>
        <FormControl fullWidth margin="normal">
          <InputLabel>Edge Type</InputLabel>
          <Select
            value={selectedEdge.type}
            onChange={(e) => updateEdge(selectedEdge.id, { type: e.target.value })}
            label="Edge Type"
          >
            <MenuItem value="default">Default</MenuItem>
            <MenuItem value="conditional">Conditional</MenuItem>
            <MenuItem value="fork">Fork</MenuItem>
            <MenuItem value="join">Join</MenuItem>
          </Select>
        </FormControl>
        {selectedEdge.type === 'conditional' && (
          <TextField
            fullWidth
            label="Condition Expression"
            value={selectedEdge.data?.conditionExpression || ''}
            onChange={(e) => 
              updateEdge(selectedEdge.id, { 
                data: { ...selectedEdge.data, conditionExpression: e.target.value }
              })
            }
            margin="normal"
            multiline
            rows={2}
          />
        )}
      </>
    );
  };

  return (
    <Paper
      sx={{
        position: 'fixed',
        right: 20,
        top: 20,
        width: 300,
        padding: 2,
        maxHeight: 'calc(100vh - 40px)',
        overflowY: 'auto',
      }}
    >
      <Box>
        {renderNodeConfig()}
        {renderEdgeConfig()}
      </Box>
    </Paper>
  );
};

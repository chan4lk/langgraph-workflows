import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Button,
  TextField,
  Box,
} from '@mui/material';
import {
  Save as SaveIcon,
  FolderOpen as OpenIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useWorkflowStore } from '../../store/workflowStore';
import { workflowApi } from '../../api/workflowApi';
import { Workflow } from '../../types/workflow';
import { LoadWorkflowDialog } from './LoadWorkflowDialog';

export const WorkflowToolbar: React.FC = () => {
  const { currentWorkflow, setCurrentWorkflow, setWorkflows } = useWorkflowStore();
  const [openLoadDialog, setOpenLoadDialog] = useState(false);
  const [workflowList, setWorkflowList] = useState<Workflow[]>([]);
  const [workflowName, setWorkflowName] = useState('');
  const [saveError, setSaveError] = useState('');

  useEffect(() => {
    if (currentWorkflow) {
      setWorkflowName(currentWorkflow.name);
    }
  }, [currentWorkflow]);

  const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setWorkflowName(event.target.value);
    if (currentWorkflow) {
      setCurrentWorkflow({
        ...currentWorkflow,
        name: event.target.value,
        updatedAt: new Date().toISOString(),
      });
    }
  };

  const handleNewWorkflow = () => {
    const newWorkflow: Workflow = {
      id: `workflow-${Date.now()}`,
      name: 'New Workflow',
      description: 'A new workflow',
      version: '1.0.0',
      nodes: [],
      edges: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setCurrentWorkflow(newWorkflow);
    setWorkflowName('New Workflow');
  };

  const handleSaveWorkflow = async () => {
    if (!currentWorkflow) return;

    try {
      setSaveError('');
      console.log('Saving workflow:', currentWorkflow);
      let savedWorkflow: Workflow;
      
      if (currentWorkflow.id) {
        savedWorkflow = await workflowApi.updateWorkflow(currentWorkflow.id, {
          ...currentWorkflow,
          updatedAt: new Date().toISOString()
        });
      } else {
        savedWorkflow = await workflowApi.createWorkflow({
          ...currentWorkflow,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        });
      }

      // Update current workflow with saved version
      setCurrentWorkflow(savedWorkflow);
      
      // Refresh workflow list
      const workflows = await workflowApi.listWorkflows();
      setWorkflows(workflows);
    } catch (error) {
      console.error('Failed to save workflow:', error);
      setSaveError('Failed to save workflow. Please try again.');
    }
  };

  const handleOpenDialog = async () => {
    try {
      const workflows = await workflowApi.listWorkflows();
      setWorkflowList(workflows);
      setOpenLoadDialog(true);
    } catch (error) {
      console.error('Failed to load workflows:', error);
    }
  };

  const handleLoadWorkflow = async (workflow: Workflow) => {
    try {
      console.log('Loading workflow:', workflow.id);
      const loadedWorkflow = await workflowApi.getWorkflow(workflow.id);
      console.log('Loaded workflow:', loadedWorkflow);
      setCurrentWorkflow(loadedWorkflow);
      setOpenLoadDialog(false);
    } catch (error) {
      console.error('Failed to load workflow:', error);
    }
  };

  const handleDeleteWorkflow = async (workflow: Workflow) => {
    if (!window.confirm('Are you sure you want to delete this workflow?')) {
      return;
    }

    try {
      await workflowApi.deleteWorkflow(workflow.id);
      const workflows = await workflowApi.listWorkflows();
      setWorkflowList(workflows);
      if (currentWorkflow?.id === workflow.id) {
        handleNewWorkflow();
      }
    } catch (error) {
      console.error('Failed to delete workflow:', error);
    }
  };

  return (
    <>
      <AppBar position="static" color="default" elevation={1} sx={{ minHeight: 64 }}>
        <Toolbar variant="dense" sx={{ minHeight: 64 }}>
          <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
            <TextField
              size="small"
              label="Workflow Name"
              value={workflowName}
              onChange={handleNameChange}
              error={!!saveError}
              helperText={saveError}
              sx={{ minWidth: 200 }}
            />
            <Button
              startIcon={<AddIcon />}
              onClick={handleNewWorkflow}
              variant="outlined"
            >
              New
            </Button>
            <Button
              startIcon={<SaveIcon />}
              onClick={handleSaveWorkflow}
              variant="outlined"
              disabled={!currentWorkflow}
            >
              Save
            </Button>
            <Button
              startIcon={<OpenIcon />}
              onClick={handleOpenDialog}
              variant="outlined"
            >
              Open
            </Button>
          </Box>
        </Toolbar>
      </AppBar>

      <LoadWorkflowDialog
        open={openLoadDialog}
        workflows={workflowList}
        onClose={() => setOpenLoadDialog(false)}
        onLoad={handleLoadWorkflow}
        onDelete={handleDeleteWorkflow}
      />
    </>
  );
};

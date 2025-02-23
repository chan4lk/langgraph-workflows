import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Stack,
  Box,
  TextField,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { useWorkflowStore } from '../../store/workflowStore';
import { NodeData, PromptTemplate, Tool, EdgeData } from '../../types/workflow';
import { TemplateManager } from '../templates/TemplateManager';
import { workflowApi } from '../../api/workflowApi';

export const ConfigPanel: React.FC = () => {
  const selectedNode = useWorkflowStore((state) => state.selectedNode);
  const selectedEdge = useWorkflowStore((state) => state.selectedEdge);
  const currentWorkflow = useWorkflowStore((state) => state.currentWorkflow);
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const updateEdge = useWorkflowStore((state) => state.updateEdge);

  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [openTemplateManager, setOpenTemplateManager] = useState(false);
  const [openToolDialog, setOpenToolDialog] = useState(false);
  const [currentTool, setCurrentTool] = useState<Tool | null>(null);

  // Load templates when component mounts
  useEffect(() => {
    loadTemplates();
  }, []);

  // Auto-save workflow when node or edge data changes
  useEffect(() => {
    if (!currentWorkflow) return;
    
    const saveTimeout = setTimeout(async () => {
      try {
        console.log('Auto-saving workflow...');
        await workflowApi.updateWorkflow(currentWorkflow.id, currentWorkflow);
        console.log('Workflow saved successfully');
      } catch (error) {
        console.error('Failed to auto-save workflow:', error);
      }
    }, 1000); // Debounce save for 1 second

    return () => clearTimeout(saveTimeout);
  }, [currentWorkflow]);

  const loadTemplates = async () => {
    try {
      const loadedTemplates = await workflowApi.listTemplates();
      console.log('Loaded templates:', loadedTemplates);
      setTemplates(loadedTemplates);
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const handleNodeUpdate = <K extends keyof NodeData>(field: K, value: NodeData[K]) => {
    if (!selectedNode) return;
    console.log('Updating node data:', field, value);
    updateNode(selectedNode.id, {
      ...selectedNode,
      data: {
        ...selectedNode.data,
        [field]: value,
      },
    });
  };

  const handleEdgeUpdate = <K extends keyof EdgeData>(field: K, value: EdgeData[K]) => {
    if (!selectedEdge) return;
    updateEdge(selectedEdge.id, {
      ...selectedEdge,
      data: {
        ...selectedEdge.data,
        [field]: value,
      },
    });
  };

  const handleToolSave = (tool: Tool) => {
    if (!selectedNode) return;
    const tools = [...(selectedNode.data.tools || [])];
    const existingIndex = tools.findIndex(t => t.id === tool.id);
    
    if (existingIndex >= 0) {
      tools[existingIndex] = tool;
    } else {
      tools.push({
        ...tool,
        id: `tool-${Date.now()}`,
      });
    }
    
    handleNodeUpdate('tools', tools);
    setOpenToolDialog(false);
    setCurrentTool(null);
  };

  const handleToolDelete = (toolId: string) => {
    if (!selectedNode?.data.tools) return;
    const tools = selectedNode.data.tools.filter(tool => tool.id !== toolId);
    handleNodeUpdate('tools', tools);
  };

  const handleTemplateSelect = async (templateId: string) => {
    if (!selectedNode) return;
    
    console.log('Selecting template:', templateId);
    
    // If empty string is selected, clear the template
    if (!templateId) {
      console.log('Clearing template');
      const updatedNode = {
        ...selectedNode,
        data: {
          ...selectedNode.data,
          promptTemplateId: '',
          template: null
        }
      };
      console.log('Updating node with cleared template:', updatedNode);
      updateNode(selectedNode.id, updatedNode);
      return;
    }

    // Find and validate template
    const template = templates.find(t => t.id === templateId);
    if (!template) {
      console.error('Template not found:', templateId);
      return;
    }

    // Update node with template
    const updatedNode = {
      ...selectedNode,
      data: {
        ...selectedNode.data,
        promptTemplateId: templateId,
        template: template
      }
    };
    console.log('Updating node with template:', updatedNode);
    updateNode(selectedNode.id, updatedNode);
    setOpenTemplateManager(false);
  };

  const renderNodeConfig = () => {
    if (!selectedNode) return null;

    switch (selectedNode.type) {
      case 'agent':
        return renderAgentConfig();
      case 'function':
        return renderFunctionConfig();
      case 'human_task':
        return renderHumanTaskConfig();
      case 'sub_workflow':
        return renderSubWorkflowConfig();
      default:
        return null;
    }
  };

  const renderAgentConfig = () => {
    if (!selectedNode) return null;
    const { data } = selectedNode;

    return (
      <Stack spacing={2}>
        <TextField
          label="Agent Name"
          value={data.agentName || ''} // Ensure value is never undefined
          onChange={(e) => handleNodeUpdate('agentName', e.target.value)}
          fullWidth
          size="small"
        />

        <TextField
          label="Description"
          value={data.description || ''} // Ensure value is never undefined
          onChange={(e) => handleNodeUpdate('description', e.target.value)}
          fullWidth
          multiline
          rows={2}
          size="small"
        />

        <FormControl fullWidth size="small">
          <InputLabel>LLM Configuration</InputLabel>
          <Select
            value={data.llmConfigId || ''} // Ensure value is never undefined
            onChange={(e) => handleNodeUpdate('llmConfigId', e.target.value)}
            label="LLM Configuration"
          >
            <MenuItem value="gpt-4">GPT-4</MenuItem>
            <MenuItem value="gpt-3.5-turbo">GPT-3.5 Turbo</MenuItem>
          </Select>
        </FormControl>
        
        {renderTemplateSelection()}
        
        {renderToolsSection()}
      </Stack>
    );
  };

  const renderFunctionConfig = () => {
    if (!selectedNode) return null;
    const { data } = selectedNode;

    return (
      <Stack spacing={2}>
        <TextField
          fullWidth
          label="Function Name"
          value={data.functionName || ''}
          onChange={(e) => handleNodeUpdate('functionName', e.target.value)}
        />
        <TextField
          fullWidth
          label="Description"
          multiline
          rows={2}
          value={data.description || ''}
          onChange={(e) => handleNodeUpdate('description', e.target.value)}
        />
      </Stack>
    );
  };

  const renderHumanTaskConfig = () => {
    if (!selectedNode) return null;
    const { data } = selectedNode;

    return (
      <Stack spacing={2}>
        <TextField
          fullWidth
          label="Task Name"
          value={data.taskName || ''}
          onChange={(e) => handleNodeUpdate('taskName', e.target.value)}
        />
        <TextField
          fullWidth
          label="Description"
          multiline
          rows={2}
          value={data.description || ''}
          onChange={(e) => handleNodeUpdate('description', e.target.value)}
        />
      </Stack>
    );
  };

  const renderSubWorkflowConfig = () => {
    if (!selectedNode) return null;
    const { data } = selectedNode;

    return (
      <Stack spacing={2}>
        <TextField
          fullWidth
          label="Workflow ID"
          value={data.workflowId || ''}
          onChange={(e) => handleNodeUpdate('workflowId', e.target.value)}
        />
        <TextField
          fullWidth
          label="Description"
          multiline
          rows={2}
          value={data.description || ''}
          onChange={(e) => handleNodeUpdate('description', e.target.value)}
        />
      </Stack>
    );
  };

  const renderEdgeConfig = () => {
    if (!selectedEdge) return null;

    return (
      <Stack spacing={2}>
        <TextField
          fullWidth
          label="Condition"
          value={selectedEdge.data?.conditionExpression || ''}
          onChange={(e) => handleEdgeUpdate('conditionExpression', e.target.value)}
        />
      </Stack>
    );
  };

  const renderTemplateSelection = () => {
    if (!selectedNode || selectedNode.type !== 'agent') return null;

    // Get template either from stored template or find by ID
    const selectedTemplate = selectedNode.data.template || 
      (selectedNode.data.promptTemplateId ? templates.find(t => t.id === selectedNode.data.promptTemplateId) : null);

    console.log('Current node data:', selectedNode.data);
    console.log('Selected template:', selectedTemplate);
    
    return (
      <Box>
        <Typography variant="subtitle1">Prompt Template</Typography>
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          <FormControl fullWidth>
            <InputLabel>Template</InputLabel>
            <Select
              value={selectedNode.data.promptTemplateId || ''}
              onChange={(e) => handleTemplateSelect(e.target.value)}
              label="Template"
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {templates.map((template) => (
                <MenuItem key={template.id} value={template.id}>
                  {template.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <IconButton 
            onClick={() => setOpenTemplateManager(true)}
            title="Manage Templates"
          >
            <SettingsIcon />
          </IconButton>
        </Box>
        {selectedTemplate && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="textSecondary">
              Template: {selectedTemplate.name}
            </Typography>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mt: 1, p: 1, bgcolor: 'grey.100', borderRadius: 1 }}>
              {selectedTemplate.content}
            </Typography>
          </Box>
        )}
      </Box>
    );
  };

  const renderToolsSection = () => {
    if (!selectedNode) return null;
    const { data } = selectedNode;

    return (
      <Box>
        <Typography variant="subtitle1">Tools</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, my: 1 }}>
          {(data.tools || []).map((tool) => (
            <Chip
              key={tool.id}
              label={tool.name}
              onDelete={() => handleToolDelete(tool.id)}
              size="small"
            />
          ))}
        </Box>
        <Button
          variant="outlined"
          size="small"
          startIcon={<AddIcon />}
          onClick={() => setOpenToolDialog(true)}
          fullWidth
        >
          Add Tool
        </Button>
      </Box>
    );
  };

  const renderToolDialog = () => {
    return (
      <Dialog
        open={openToolDialog}
        onClose={() => {
          setOpenToolDialog(false);
          setCurrentTool(null);
        }}
      >
        <DialogTitle>
          {currentTool ? 'Edit Tool' : 'Add Tool'}
        </DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Name"
              value={currentTool?.name || ''}
              onChange={(e) => setCurrentTool((prev: Tool | null) => prev ? { ...prev, name: e.target.value } : { 
                id: `tool-${Date.now()}`,
                name: e.target.value,
                description: '',
                type: 'function',
              })}
            />
            <TextField
              fullWidth
              label="Description"
              multiline
              rows={2}
              value={currentTool?.description || ''}
              onChange={(e) => setCurrentTool((prev: Tool | null) => prev ? { ...prev, description: e.target.value } : null)}
            />
            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                value={currentTool?.type || ''}
                label="Type"
                onChange={(e) => setCurrentTool((prev: Tool | null) => prev ? { 
                  ...prev, 
                  type: e.target.value as 'function' | 'api' | 'custom'
                } : null)}
              >
                <MenuItem value="function">Function</MenuItem>
                <MenuItem value="api">API</MenuItem>
                <MenuItem value="custom">Other</MenuItem>
              </Select>
            </FormControl>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setOpenToolDialog(false);
            setCurrentTool(null);
          }}>
            Cancel
          </Button>
          <Button
            onClick={() => handleToolSave(currentTool as Tool)}
            variant="contained"
            disabled={!currentTool?.name || !currentTool?.type}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    );
  };

  return (
    <Paper 
      sx={{ 
        position: 'absolute',
        right: 20,
        top: 20,
        width: 300,
        maxHeight: 'calc(100vh - 100px)',
        overflowY: 'auto',
        p: 2,
        zIndex: 1000,
        display: selectedNode || selectedEdge ? 'block' : 'none',
      }}
    >
      <Stack spacing={3}>
        {selectedNode && (
          <>
            <Typography variant="h6" gutterBottom>
              Node Configuration
            </Typography>
            {renderNodeConfig()}
          </>
        )}
        {selectedEdge && (
          <>
            <Typography variant="h6" gutterBottom>
              Edge Configuration
            </Typography>
            {renderEdgeConfig()}
          </>
        )}
        {renderToolDialog()}
        <TemplateManager
          open={openTemplateManager}
          onClose={() => setOpenTemplateManager(false)}
          onSelect={handleTemplateSelect}
          selectedTemplateId={selectedNode?.data.promptTemplateId}
        />
      </Stack>
    </Paper>
  );
};

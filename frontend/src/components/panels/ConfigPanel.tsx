import React, { useState, useEffect } from 'react';
import { Box, Stack, Typography, FormControl, InputLabel, Select, MenuItem, IconButton, Chip } from '@mui/material';
import { useWorkflowStore } from '../../store/workflowStore';
import { NodeData, PromptTemplate, NodeType } from '../../types/workflow';
import { EdgeData } from '../../types/workflow';
import { TemplateManager } from '../templates/TemplateManager';
import { templateApi } from '../../api/templateApi';
import { NodeFactory } from '../../nodes/NodeFactory';
import { NodeConfig } from './NodeConfig';
import { EdgeConfig } from './EdgeConfig';
import { workflowApi } from '../../api/workflowApi';
import { Tool } from '../../types/tool';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';

export const ConfigPanel = () => {
  const selectedNode = useWorkflowStore((state) => state.selectedNode);
  const selectedEdge = useWorkflowStore((state) => state.selectedEdge);
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const updateEdge = useWorkflowStore((state) => state.updateEdge);

  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [openTemplateManager, setOpenTemplateManager] = useState(false);
  const [tools, setTools] = useState<Tool[]>([]);
  const [selectedTools, setSelectedTools] = useState<Tool[]>([]);

  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const loadedTemplates = await templateApi.listTemplates();
        setTemplates(loadedTemplates);
      } catch (error) {
        console.error('Failed to load templates:', error);
      }
    };
    loadTemplates();
  }, []);

  useEffect(() => {
    const loadTools = async () => {
      try {
        const toolsData = await workflowApi.getTools();
        setTools(toolsData);
      } catch (error) {
        console.error('Failed to load tools:', error);
      }
    };
    loadTools();
  }, []);

  useEffect(() => {
    if (selectedNode?.data.tools) {
      setSelectedTools(selectedNode.data.tools);
    } else {
      setSelectedTools([]);
    }
  }, [selectedNode]);

  const handleNodeUpdate = (field: keyof NodeData, value: any) => {
    if (!selectedNode) return;

    const nodeFactory = NodeFactory.getInstance();
    const updatedData = nodeFactory.updateData(
      selectedNode.data.type,
      selectedNode.data,
      { [field]: value }
    );

    updateNode(selectedNode.id, {
      ...selectedNode,
      data: updatedData,
    });
  };

  const handleEdgeUpdate = (field: keyof EdgeData, value: any) => {
    if (!selectedEdge) return;
    updateEdge(selectedEdge.id, {
      ...selectedEdge,
      data: {
        ...selectedEdge.data,
        [field]: value,
      },
    });
  };

  const handleTemplateSelect = async (templateId: string) => {
    try {
      const template = await templateApi.getTemplate(templateId);
      if (template && selectedNode) {
        handleNodeUpdate('template', template);
      }
    } catch (error) {
      console.error('Failed to load template:', error);
    }
  };

  const handleToolSelect = (toolId: string) => {
    const tool = tools.find(t => t.id === toolId);
    if (tool && !selectedTools.some(t => t.id === tool.id)) {
      const newTools = [...selectedTools, tool];
      setSelectedTools(newTools);
      handleNodeUpdate('tools', newTools);
    }
  };

  const handleToolRemove = (toolId: string) => {
    const newTools = selectedTools.filter(t => t.id !== toolId);
    setSelectedTools(newTools);
    handleNodeUpdate('tools', newTools);
  };

  const renderToolConfig = () => {
    if (!selectedNode || selectedNode.data.type !== NodeType.TOOL) return null;

    return (
      <Stack spacing={2}>
        <Typography variant="subtitle2">Tools</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {selectedTools.map((tool) => (
            <Chip
              key={tool.id}
              label={tool.name}
              onDelete={() => handleToolRemove(tool.id)}
              deleteIcon={<DeleteIcon />}
              title={tool.description}
            />
          ))}
        </Box>
        <FormControl fullWidth>
          <InputLabel>Add Tool</InputLabel>
          <Select
            value=""
            label="Add Tool"
            onChange={(e) => handleToolSelect(e.target.value)}
          >
            {tools
              .filter((tool) => !selectedTools.some((t) => t.id === tool.id))
              .map((tool) => (
                <MenuItem key={tool.id} value={tool.id}>
                  <Box>
                    <Typography>{tool.name}</Typography>
                    <Typography variant="caption" color="textSecondary">
                      {tool.description}
                    </Typography>
                  </Box>
                </MenuItem>
              ))}
          </Select>
        </FormControl>
      </Stack>
    );
  };

  return (
    <Box sx={{ p: 2, width: '100%' }}>
      {selectedNode && (
        <>
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6">Node Configuration</Typography>
          </Box>
          <Stack spacing={3}>
            <NodeConfig
              node={selectedNode}
              templates={templates}
              onNodeUpdate={handleNodeUpdate}
              onTemplateSelect={handleTemplateSelect}
              onOpenTemplateManager={() => setOpenTemplateManager(true)}
            />
            {renderToolConfig()}
          </Stack>
        </>
      )}
      {selectedEdge && (
        <>
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6">Edge Configuration</Typography>
          </Box>
          <EdgeConfig
            edge={selectedEdge}
            onEdgeUpdate={handleEdgeUpdate}
          />
        </>
      )}
      <TemplateManager
        open={openTemplateManager}
        onClose={() => setOpenTemplateManager(false)}
        onSelect={handleTemplateSelect}
        onTemplatesChange={setTemplates}
        selectedTemplateId={selectedNode?.data.template?.id}
      />
    </Box>
  );
};

import React, { useState, useEffect } from 'react';
import { Box } from '@mui/material';
import { useWorkflowStore } from '../../store/workflowStore';
import { NodeData, PromptTemplate } from '../../types/workflow';
import { EdgeData } from '../../types/workflow';
import { TemplateManager } from '../templates/TemplateManager';
import { templateApi } from '../../api/templateApi';
import { NodeFactory } from '../../nodes/NodeFactory';
import { NodeConfig } from './NodeConfig';
import { EdgeConfig } from './EdgeConfig';

export const ConfigPanel = () => {
  const selectedNode = useWorkflowStore((state) => state.selectedNode);
  const selectedEdge = useWorkflowStore((state) => state.selectedEdge);
  const updateNode = useWorkflowStore((state) => state.updateNode);
  const updateEdge = useWorkflowStore((state) => state.updateEdge);

  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [openTemplateManager, setOpenTemplateManager] = useState(false);

  console.log('selectedNode:', selectedNode);
  console.log('selectedEdge:', selectedEdge);

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

  return (
    <Box sx={{ p: 2, width: '100%' }}>
      {selectedNode && (
        <>
          <Box sx={{ mb: 2 }}>
            <strong>Node Configuration</strong>
          </Box>
          <NodeConfig
            node={selectedNode}
            templates={templates}
            onNodeUpdate={handleNodeUpdate}
            onTemplateSelect={handleTemplateSelect}
            onOpenTemplateManager={() => setOpenTemplateManager(true)}
          />
        </>
      )}
      {selectedEdge && (
        <>
          <Box sx={{ mb: 2 }}>
            <strong>Edge Configuration</strong>
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

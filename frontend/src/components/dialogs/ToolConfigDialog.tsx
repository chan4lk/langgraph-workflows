import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import { NodeData, NodeTool } from '../../types/workflow';
import { Tool } from '../../types/tool';
import { ToolSelect } from '../panels/ToolSelect';

interface ToolConfigDialogProps {
  open: boolean;
  node: NodeData;
  tools: Tool[];
  onClose: () => void;
  onSave: (updates: Partial<NodeData>) => void;
  onToolsUpdate?: (nodeId: string, tools: NodeTool[]) => void;
}

export const ToolConfigDialog: React.FC<ToolConfigDialogProps> = ({
  open,
  node,
  tools,
  onClose,
  onSave,
  onToolsUpdate,
}) => {
  const [selectedTools, setSelectedTools] = useState<NodeTool[]>(node.tools || []);

  const handleToolsChange = (tools: NodeTool[]) => {
    setSelectedTools(tools);
    if (onToolsUpdate) {
      onToolsUpdate(node.id, tools);
    }
  };

  const handleSave = () => {
    onSave({
      ...node,
      tools: selectedTools,
    });
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Configure Tool Node</DialogTitle>
      <DialogContent>
        <ToolSelect
          selectedTools={selectedTools}
          availableTools={tools}
          onToolsChange={handleToolsChange}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave} variant="contained" color="primary">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

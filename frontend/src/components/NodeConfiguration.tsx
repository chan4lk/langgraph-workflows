import React from 'react';
import { NodeData, NodeTool } from '../types/workflow';
import { ToolConfigDialog } from './dialogs/ToolConfigDialog';
import { Tool } from '../types/tool';

interface NodeConfigurationProps {
  open: boolean;
  node: NodeData;
  onClose: () => void;
  onSave: (updates: Partial<NodeData>) => void;
  onToolsUpdate?: (nodeId: string, tools: NodeTool[]) => void;
  tools: Tool[];
}

export const NodeConfiguration: React.FC<NodeConfigurationProps> = ({
  open,
  node,
  onClose,
  onSave,
  onToolsUpdate,
  tools,
}) => {
  if (node.type === 'tool') {
    return (
      <ToolConfigDialog
        open={open}
        node={node}
        tools={tools}
        onClose={onClose}
        onSave={onSave}
        onToolsUpdate={onToolsUpdate}
      />
    );
  }

  // Add other node type configurations here
  return null;
};

import React from 'react';
import {
  Stack,
  TextField,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Settings as SettingsIcon } from '@mui/icons-material';
import { NodeData, PromptTemplate, NodeType } from '../../types/workflow';
import { WorkflowNode } from '../../types/workflow';

interface NodeConfigProps {
  node: WorkflowNode;
  templates: PromptTemplate[];
  onNodeUpdate: (field: keyof NodeData, value: any) => void;
  onTemplateSelect: (templateId: string) => void;
  onOpenTemplateManager: () => void;
}

export const NodeConfig: React.FC<NodeConfigProps> = ({
  node,
  templates,
  onNodeUpdate,
  onTemplateSelect,
  onOpenTemplateManager,
}) => {
  const data = node.data;
  const type = data.type;

  return (
    <Stack spacing={2}>
      <TextField
        fullWidth
        label="Label"
        value={data.label || ''}
        onChange={(e) => onNodeUpdate('label', e.target.value)}
      />
      
      {type === NodeType.AGENT && (
        <TextField
          fullWidth
          label="System Prompt"
          multiline
          rows={4}
          value={data.systemPrompt || ''}
          onChange={(e) => onNodeUpdate('systemPrompt', e.target.value)}
        />
      )}
      
      {(type === NodeType.AGENT || type === NodeType.FUNCTION) && (
        <FormControl fullWidth>
          <InputLabel>Template</InputLabel>
          <Select
            value={data.template?.id || ''}
            onChange={(e) => onTemplateSelect(e.target.value)}
            label="Template"
            endAdornment={
              <IconButton
                size="small"
                onClick={onOpenTemplateManager}
                sx={{ mr: 2 }}
              >
                <SettingsIcon />
              </IconButton>
            }
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
      )}
    </Stack>
  );
};

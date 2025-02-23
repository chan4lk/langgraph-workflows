import React from 'react';
import {
  FormControl,
  FormLabel,
  Select,
  MenuItem,
  Stack,
  Chip,
  Box,
  SelectChangeEvent,
} from '@mui/material';
import { Tool } from '../../types/tool';
import { NodeTool } from '../../types/workflow';

interface ToolSelectProps {
  selectedTools: NodeTool[];
  availableTools: Tool[];
  onToolsChange: (tools: NodeTool[]) => void;
}

export const ToolSelect: React.FC<ToolSelectProps> = ({
  selectedTools,
  availableTools,
  onToolsChange,
}) => {
  const handleToolSelect = (event: SelectChangeEvent<string>) => {
    const selectedToolId = event.target.value;
    if (!selectedToolId) return;

    const tool = availableTools.find((t) => t.id === selectedToolId);
    if (!tool) return;

    // Convert to NodeTool by omitting timestamps
    const nodeTool: NodeTool = {
      id: tool.id,
      name: tool.name,
      description: tool.description,
      type: tool.type,
      config: tool.config,
    };

    onToolsChange([...selectedTools, nodeTool]);
  };

  const handleToolDelete = (toolId: string) => {
    onToolsChange(selectedTools.filter((tool) => tool.id !== toolId));
  };

  return (
    <FormControl fullWidth>
      <FormLabel>Tools</FormLabel>
      <Stack spacing={2}>
        <Select
          value=""
          onChange={handleToolSelect}
          displayEmpty
          fullWidth
        >
          <MenuItem value="" disabled>
            Select a tool...
          </MenuItem>
          {availableTools
            .filter((tool) => !selectedTools.some((st) => st.id === tool.id))
            .map((tool) => (
              <MenuItem key={tool.id} value={tool.id}>
                {tool.name}
              </MenuItem>
            ))}
        </Select>

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {selectedTools.map((tool) => (
            <Chip
              key={tool.id}
              label={tool.name}
              onDelete={() => handleToolDelete(tool.id)}
              color="primary"
              variant="outlined"
            />
          ))}
        </Box>
      </Stack>
    </FormControl>
  );
};

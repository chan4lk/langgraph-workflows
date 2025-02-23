import React from 'react';
import { NodeProps } from 'reactflow';
import { Api, Code } from '@mui/icons-material';
import { Box, Chip, Typography } from '@mui/material';
import { BaseNode } from './BaseNode';
import { WorkflowNode } from '../../types/workflow';
import { ToolType } from '../../types/tool';

interface ToolNodeProps extends NodeProps {
  data: WorkflowNode['data'];
}

export const ToolNode: React.FC<ToolNodeProps> = (props) => {
  const getToolIcon = () => {
    if (props.data.toolConfig?.type === ToolType.API) {
      return <Api color="primary" />;
    }
    return <Code color="primary" />;
  };

  const getToolType = () => {
    const type = props.data.toolConfig?.type;
    if (!type) return null;

    return (
      <Chip
        label={type === ToolType.API ? 'API Tool' : 'Code Block'}
        size="small"
        color="secondary"
        sx={{ ml: 1 }}
      />
    );
  };

  const getToolDetails = () => {
    const config = props.data.toolConfig;
    if (!config) return null;

    if (config.type === ToolType.API) {
      const apiConfig = config.api_config;
      if (!apiConfig) return null;

      return (
        <>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Chip 
              label={apiConfig.method} 
              size="small" 
              color="primary" 
              variant="outlined"
              sx={{ mr: 1 }}
            />
            <Typography variant="body2" noWrap>
              {apiConfig.url}
            </Typography>
          </Box>
          {apiConfig.parameters.length > 0 && (
            <Typography variant="caption" color="text.secondary" display="block">
              Parameters: {apiConfig.parameters.map(p => p.name).join(', ')}
            </Typography>
          )}
        </>
      );
    }

    if (config.type === ToolType.CODE_BLOCK) {
      const codeConfig = config.code_block_config;
      if (!codeConfig) return null;

      return (
        <>
          <Typography variant="body2" fontFamily="monospace" sx={{ mb: 1 }}>
            {codeConfig.function_name}()
          </Typography>
          {codeConfig.parameters.length > 0 && (
            <Typography variant="caption" color="text.secondary" display="block">
              Parameters: {codeConfig.parameters.map(p => p.name).join(', ')}
            </Typography>
          )}
          {codeConfig.return_type && (
            <Typography variant="caption" color="text.secondary" display="block">
              Returns: {codeConfig.return_type}
            </Typography>
          )}
        </>
      );
    }

    return null;
  };

  return (
    <BaseNode {...props}>
      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, mt: 1 }}>
        {getToolIcon()}
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="body2" fontWeight="medium">
              Tool: {props.data.toolId}
            </Typography>
            {getToolType()}
          </Box>
          {props.data.description && (
            <Typography 
              variant="caption" 
              color="text.secondary" 
              display="block" 
              sx={{ mt: 0.5, mb: 1 }}
            >
              {props.data.description}
            </Typography>
          )}
          {getToolDetails()}
        </Box>
      </Box>
    </BaseNode>
  );
};

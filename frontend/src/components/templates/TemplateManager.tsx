import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  IconButton,
  TextField,
  Stack,
  Typography,
  Divider,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { PromptTemplate } from '../../types/workflow';
import { workflowApi } from '../../api/workflowApi';

interface TemplateManagerProps {
  open: boolean;
  onClose: () => void;
  onSelect?: (templateId: string) => void;
  selectedTemplateId?: string;
}

export const TemplateManager: React.FC<TemplateManagerProps> = ({
  open,
  onClose,
  onSelect,
  selectedTemplateId,
}) => {
  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [editTemplate, setEditTemplate] = useState<Partial<PromptTemplate> | null>(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);

  useEffect(() => {
    if (open) {
      loadTemplates();
    }
  }, [open]);

  const loadTemplates = async () => {
    try {
      const loadedTemplates = await workflowApi.listTemplates();
      setTemplates(loadedTemplates);
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const handleSaveTemplate = async () => {
    if (!editTemplate?.name || !editTemplate?.content) return;

    try {
      if (editTemplate.id) {
        // Update existing template
        await workflowApi.updateTemplate(editTemplate.id, {
          ...editTemplate,
          createdAt: editTemplate.createdAt || new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        } as PromptTemplate);
      } else {
        // Create new template
        const newTemplate = {
          ...editTemplate,
          id: `template-${Date.now()}`,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        } as PromptTemplate;
        await workflowApi.createTemplate(newTemplate);
      }
      await loadTemplates();
      setEditDialogOpen(false);
      setEditTemplate(null);
    } catch (error) {
      console.error('Failed to save template:', error);
    }
  };

  const handleDeleteTemplate = async (templateId: string) => {
    if (!window.confirm('Are you sure you want to delete this template?')) return;

    try {
      await workflowApi.deleteTemplate(templateId);
      await loadTemplates();
    } catch (error) {
      console.error('Failed to delete template:', error);
    }
  };

  const renderEditDialog = () => (
    <Dialog
      open={editDialogOpen}
      onClose={() => {
        setEditDialogOpen(false);
        setEditTemplate(null);
      }}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle>
        {editTemplate?.id ? 'Edit Template' : 'Create Template'}
      </DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 2 }}>
          <TextField
            fullWidth
            label="Name"
            value={editTemplate?.name || ''}
            onChange={(e) => setEditTemplate(prev => ({ ...prev, name: e.target.value }))}
          />
          <TextField
            fullWidth
            label="Description"
            multiline
            rows={2}
            value={editTemplate?.description || ''}
            onChange={(e) => setEditTemplate(prev => ({ ...prev, description: e.target.value }))}
          />
          <TextField
            fullWidth
            label="Content"
            multiline
            rows={4}
            value={editTemplate?.content || ''}
            onChange={(e) => setEditTemplate(prev => ({ ...prev, content: e.target.value }))}
          />
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => {
          setEditDialogOpen(false);
          setEditTemplate(null);
        }}>
          Cancel
        </Button>
        <Button
          onClick={handleSaveTemplate}
          variant="contained"
          disabled={!editTemplate?.name || !editTemplate?.content}
        >
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <>
      <Dialog
        open={open}
        onClose={onClose}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">Prompt Templates</Typography>
            <Button
              startIcon={<AddIcon />}
              onClick={() => {
                setEditTemplate({});
                setEditDialogOpen(true);
              }}
            >
              Create Template
            </Button>
          </Stack>
        </DialogTitle>
        <Divider />
        <DialogContent>
          <List>
            {templates.map((template) => (
              <ListItem
                disablePadding
                key={template.id}
                secondaryAction={
                  <IconButton
                    edge="end"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteTemplate(template.id);
                    }}
                  >
                    <DeleteIcon />
                  </IconButton>
                }
              >
                <ListItemButton
                  onClick={() => onSelect?.(template.id)}
                  selected={template.id === selectedTemplateId}
                  sx={{
                    '&.Mui-selected': {
                      backgroundColor: 'primary.light',
                      '&:hover': {
                        backgroundColor: 'primary.light',
                      },
                    },
                    cursor: onSelect ? 'pointer' : 'default',
                  }}
                >
                  <ListItemText
                    primary={
                      <Typography
                        variant="body1"
                        color={template.id === selectedTemplateId ? 'primary' : 'text.primary'}
                      >
                        {template.name}
                      </Typography>
                    }
                    secondary={
                      <Typography
                        variant="body2"
                        color={template.id === selectedTemplateId ? 'primary.dark' : 'text.secondary'}
                        sx={{ 
                          display: '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: 'vertical',
                          overflow: 'hidden',
                        }}
                      >
                        {template.description || template.content.substring(0, 100)}
                      </Typography>
                    }
                  />
                  <IconButton
                    edge="end"
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditTemplate(template);
                      setEditDialogOpen(true);
                    }}
                  >
                    <EditIcon />
                  </IconButton>
                </ListItemButton>
              </ListItem>
            ))}
            {templates.length === 0 && (
              <ListItem>
                <ListItemText
                  primary="No templates available"
                  secondary="Click 'Create Template' to add one"
                />
              </ListItem>
            )}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
      {renderEditDialog()}
    </>
  );
};

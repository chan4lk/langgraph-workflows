import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Button,
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import { Workflow } from '../../types/workflow';

interface LoadWorkflowDialogProps {
  open: boolean;
  workflows: Workflow[];
  onClose: () => void;
  onLoad: (workflow: Workflow) => void;
  onDelete: (workflow: Workflow) => void;
}

export const LoadWorkflowDialog: React.FC<LoadWorkflowDialogProps> = ({
  open,
  workflows,
  onClose,
  onLoad,
  onDelete,
}) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Open Workflow</DialogTitle>
      <DialogContent>
        <List>
          {workflows.map((workflow) => (
            <ListItem
              key={workflow.id}
              secondaryAction={
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={() => onDelete(workflow)}
                >
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemText
                primary={workflow.name}
                secondary={`Last modified: ${new Date(workflow.updatedAt).toLocaleString()}`}
                onClick={() => onLoad(workflow)}
                sx={{ cursor: 'pointer' }}
              />
            </ListItem>
          ))}
          {workflows.length === 0 && (
            <ListItem>
              <ListItemText primary="No workflows found" />
            </ListItem>
          )}
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

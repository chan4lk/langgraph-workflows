import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  Grid, 
  Chip,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { 
  ArrowBack as ArrowBackIcon, 
  Edit as EditIcon, 
  Delete as DeleteIcon,
  Storage as StorageIcon,
  CloudUpload as CloudUploadIcon,
  TableChart as TableChartIcon,
  Schedule as ScheduleIcon,
  CalendarToday as CalendarTodayIcon,
  AccessTime as AccessTimeIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { Pipeline } from '../../types/dataPipeline';

// Mock data for demonstration
const mockPipeline: Pipeline = {
  id: '1',
  name: 'Data Sync Pipeline',
  createdOn: 'Jan 15, 2025',
  source: {
    type: 'PostgreSQL Database',
    name: 'users_table',
    details: {
      connection: 'db.example.com'
    }
  },
  destination: {
    type: 'Amazon S3',
    name: 'bucket/data/users/',
    format: 'CSV Format'
  },
  schedule: {
    frequency: 'Every 6 hours',
    days: ['All days'],
    timezone: 'UTC+00:00'
  },
  executionHistory: [
    {
      status: 'successful',
      timestamp: 'Jan 20, 2025 14:30:00',
      recordsProcessed: 1234
    },
    {
      status: 'successful',
      timestamp: 'Jan 20, 2025 08:30:00',
      recordsProcessed: 1156
    },
    {
      status: 'failed',
      timestamp: 'Jan 20, 2025 02:30:00',
      errorMessage: 'Connection timeout error'
    }
  ]
};

export const PipelineDetails: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [pipeline, setPipeline] = useState<Pipeline | null>(null);

  useEffect(() => {
    // In a real app, you would fetch the pipeline data from your API
    // For now, we'll use mock data
    setPipeline(mockPipeline);
  }, [id]);

  if (!pipeline) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography>Loading pipeline details...</Typography>
      </Box>
    );
  }

  const handleDelete = () => {
    // In a real app, you would call your API to delete the pipeline
    // For now, we'll just navigate back to the list
    if (window.confirm('Are you sure you want to delete this pipeline?')) {
      navigate('/pipelines');
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: '1200px', margin: '0 auto' }}>
      <Box sx={{ mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/pipelines')}
          sx={{ mb: 2 }}
        >
          Back to Pipelines
        </Button>
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Pipeline Details
        </Typography>
        <Box>
          <IconButton color="primary" onClick={() => navigate(`/pipelines/${id}/edit`)}>
            <EditIcon />
          </IconButton>
          <IconButton color="error" onClick={handleDelete}>
            <DeleteIcon />
          </IconButton>
        </Box>
      </Box>

      <Paper sx={{ p: 4, mb: 4 }}>
        <Typography variant="h5" sx={{ mb: 2 }}>
          {pipeline.name}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Created on {pipeline.createdOn}
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Source
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <StorageIcon />
                </ListItemIcon>
                <ListItemText 
                  primary={pipeline.source.type} 
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  inset
                  primary={pipeline.source.details?.connection} 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TableChartIcon />
                </ListItemIcon>
                <ListItemText 
                  primary={pipeline.source.name} 
                />
              </ListItem>
            </List>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Destination
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <CloudUploadIcon />
                </ListItemIcon>
                <ListItemText 
                  primary={pipeline.destination.type} 
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  inset
                  primary={pipeline.destination.name} 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TableChartIcon />
                </ListItemIcon>
                <ListItemText 
                  primary={pipeline.destination.format} 
                />
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 4, mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Schedule Details
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <ScheduleIcon />
                </ListItemIcon>
                <ListItemText primary={pipeline.schedule.frequency} />
              </ListItem>
            </List>
          </Grid>
          <Grid item xs={12} md={4}>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <CalendarTodayIcon />
                </ListItemIcon>
                <ListItemText primary={pipeline.schedule.days?.join(', ')} />
              </ListItem>
            </List>
          </Grid>
          <Grid item xs={12} md={4}>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <AccessTimeIcon />
                </ListItemIcon>
                <ListItemText primary={pipeline.schedule.timezone} />
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Execution History
        </Typography>
        <List>
          {pipeline.executionHistory?.map((execution, index) => (
            <React.Fragment key={index}>
              {index > 0 && <Divider component="li" />}
              <ListItem alignItems="flex-start">
                <ListItemIcon>
                  {execution.status === 'successful' ? 
                    <CheckCircleIcon color="success" /> : 
                    <ErrorIcon color="error" />
                  }
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Box>
                        <Chip 
                          label={execution.status} 
                          color={execution.status === 'successful' ? 'success' : 'error'}
                          size="small"
                          sx={{ mr: 1 }}
                        />
                        {execution.status === 'successful' && execution.recordsProcessed && 
                          `Processed ${execution.recordsProcessed.toLocaleString()} records`
                        }
                        {execution.status === 'failed' && execution.errorMessage && 
                          execution.errorMessage
                        }
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {execution.timestamp}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            </React.Fragment>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

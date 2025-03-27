import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Chip
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { Pipeline } from '../../types/dataPipeline';

// Mock data for demonstration
const mockPipelines: Pipeline[] = [
  {
    id: '1',
    name: 'Data Sync Pipeline',
    createdOn: '2025-01-15',
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
        timestamp: '2025-01-20T14:30:00',
        recordsProcessed: 1234
      },
      {
        status: 'successful',
        timestamp: '2025-01-20T08:30:00',
        recordsProcessed: 1156
      },
      {
        status: 'failed',
        timestamp: '2025-01-20T02:30:00',
        errorMessage: 'Connection timeout error'
      }
    ]
  }
];

export const PipelineList: React.FC = () => {
  const navigate = useNavigate();
  const [pipelines] = useState<Pipeline[]>(mockPipelines);

  return (
    <Box sx={{ p: 3, maxWidth: '1200px', margin: '0 auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Data Pipelines
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />}
          onClick={() => navigate('/pipelines/create')}
        >
          Create Pipeline
        </Button>
      </Box>

      {pipelines.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            No pipelines found. Create your first pipeline to get started.
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Pipeline Name</TableCell>
                <TableCell>Source</TableCell>
                <TableCell>Destination</TableCell>
                <TableCell>Schedule</TableCell>
                <TableCell>Last Status</TableCell>
                <TableCell>Created On</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {pipelines.map((pipeline) => (
                <TableRow 
                  key={pipeline.id}
                  hover
                  onClick={() => navigate(`/pipelines/${pipeline.id}`)}
                  sx={{ cursor: 'pointer' }}
                >
                  <TableCell>{pipeline.name}</TableCell>
                  <TableCell>{pipeline.source.type}</TableCell>
                  <TableCell>{pipeline.destination.type}</TableCell>
                  <TableCell>{pipeline.schedule.frequency}</TableCell>
                  <TableCell>
                    {pipeline.executionHistory && pipeline.executionHistory.length > 0 && (
                      <Chip 
                        label={pipeline.executionHistory[0].status} 
                        color={pipeline.executionHistory[0].status === 'successful' ? 'success' : 'error'}
                        size="small"
                      />
                    )}
                  </TableCell>
                  <TableCell>{pipeline.createdOn}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

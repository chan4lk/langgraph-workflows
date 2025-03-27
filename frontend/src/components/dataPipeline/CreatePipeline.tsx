import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  TextField, 
  Grid, 
  MenuItem, 
  Select, 
  FormControl, 
  InputLabel,
  FormHelperText,
  IconButton
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, AccessTime as AccessTimeIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

type SourceType = 'postgres' | 'mysql' | 'mongodb' | 'api';
type DestinationType = 's3' | 'bigquery' | 'snowflake' | 'local';
type FrequencyType = 'hourly' | 'daily' | 'weekly' | 'monthly';

interface FormData {
  name: string;
  source: SourceType | '';
  destination: DestinationType | '';
  frequency: FrequencyType | '';
  startTime: string;
}

export const CreatePipeline: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    name: '',
    source: '',
    destination: '',
    frequency: '',
    startTime: '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({});

  const handleChange = (field: keyof FormData) => (
    event: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
    
    // Clear error when field is edited
    if (errors[field]) {
      setErrors({
        ...errors,
        [field]: undefined,
      });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {};
    
    if (!formData.name) newErrors.name = 'Pipeline name is required';
    if (!formData.source) newErrors.source = 'Source is required';
    if (!formData.destination) newErrors.destination = 'Destination is required';
    if (!formData.frequency) newErrors.frequency = 'Frequency is required';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    
    if (validateForm()) {
      // Here you would typically submit the data to your backend
      console.log('Submitting pipeline:', formData);
      
      // Navigate back to the pipeline list
      navigate('/pipelines');
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: '900px', margin: '0 auto' }}>
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/pipelines')}
          sx={{ mb: 2 }}
        >
          Back to Pipelines
        </Button>
        <Typography variant="h4" component="h1">
          Create New Pipeline
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Configure your data pipeline by filling in the details below
        </Typography>
      </Box>

      <Paper sx={{ p: 4 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={4}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Pipeline Name"
                placeholder="Enter pipeline name"
                value={formData.name}
                onChange={handleChange('name')}
                error={!!errors.name}
                helperText={errors.name}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth error={!!errors.source}>
                <InputLabel id="source-label">Source</InputLabel>
                <Select
                  labelId="source-label"
                  value={formData.source}
                  label="Source"
                  onChange={handleChange('source') as any}
                  displayEmpty
                  renderValue={formData.source ? undefined : () => "Select source"}
                >
                  <MenuItem value="postgres">PostgreSQL Database</MenuItem>
                  <MenuItem value="mysql">MySQL Database</MenuItem>
                  <MenuItem value="mongodb">MongoDB</MenuItem>
                  <MenuItem value="api">REST API</MenuItem>
                </Select>
                {errors.source && <FormHelperText>{errors.source}</FormHelperText>}
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth error={!!errors.destination}>
                <InputLabel id="destination-label">Destination</InputLabel>
                <Select
                  labelId="destination-label"
                  value={formData.destination}
                  label="Destination"
                  onChange={handleChange('destination') as any}
                  displayEmpty
                  renderValue={formData.destination ? undefined : () => "Select destination"}
                >
                  <MenuItem value="s3">Amazon S3</MenuItem>
                  <MenuItem value="bigquery">Google BigQuery</MenuItem>
                  <MenuItem value="snowflake">Snowflake</MenuItem>
                  <MenuItem value="local">Local Storage</MenuItem>
                </Select>
                {errors.destination && <FormHelperText>{errors.destination}</FormHelperText>}
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Schedule Configuration
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth error={!!errors.frequency}>
                <InputLabel id="frequency-label">Frequency</InputLabel>
                <Select
                  labelId="frequency-label"
                  value={formData.frequency}
                  label="Frequency"
                  onChange={handleChange('frequency') as any}
                  displayEmpty
                  renderValue={formData.frequency ? undefined : () => "Select frequency"}
                >
                  <MenuItem value="hourly">Hourly</MenuItem>
                  <MenuItem value="daily">Daily</MenuItem>
                  <MenuItem value="weekly">Weekly</MenuItem>
                  <MenuItem value="monthly">Monthly</MenuItem>
                </Select>
                {errors.frequency && <FormHelperText>{errors.frequency}</FormHelperText>}
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Start Time"
                type="time"
                value={formData.startTime}
                onChange={handleChange('startTime')}
                InputProps={{
                  endAdornment: (
                    <IconButton edge="end">
                      <AccessTimeIcon />
                    </IconButton>
                  ),
                }}
                inputProps={{
                  step: 300, // 5 min
                }}
              />
            </Grid>

            <Grid item xs={12} sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <Button 
                variant="outlined" 
                onClick={() => navigate('/pipelines')}
              >
                Cancel
              </Button>
              <Button 
                variant="contained" 
                type="submit"
              >
                Create Pipeline
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
};

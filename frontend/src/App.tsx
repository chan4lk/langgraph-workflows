import React from 'react';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Layouts
import { MainLayout } from './components/MainLayout';
import { WorkflowLayout } from './components/WorkflowLayout';
import { PipelineLayout } from './components/dataPipeline/PipelineLayout';

// Data Pipeline Components
import { PipelineList } from './components/dataPipeline/PipelineList';
import { CreatePipeline } from './components/dataPipeline/CreatePipeline';
import { PipelineDetails } from './components/dataPipeline/PipelineDetails';

const theme = createTheme({
  palette: {
    mode: 'light',
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: '0px 2px 4px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

export const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            {/* Workflow Designer Routes */}
            <Route index element={<WorkflowLayout />} />
            
            {/* Data Pipeline Routes */}
            <Route path="pipelines" element={<PipelineLayout />}>
              <Route index element={<PipelineList />} />
              <Route path="create" element={<CreatePipeline />} />
              <Route path=":id" element={<PipelineDetails />} />
            </Route>
            
            {/* Fallback route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
};

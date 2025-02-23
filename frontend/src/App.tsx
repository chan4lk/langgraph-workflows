import React from 'react';
import { CssBaseline, ThemeProvider, createTheme, Box } from '@mui/material';
import { ReactFlowProvider } from 'reactflow';
import { WorkflowDesigner } from './components/WorkflowDesigner';
import { WorkflowToolbar } from './components/toolbar/WorkflowToolbar';

const theme = createTheme({
  palette: {
    mode: 'light',
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
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
      <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        <WorkflowToolbar />
        <Box sx={{ flexGrow: 1, position: 'relative' }}>
          <ReactFlowProvider>
            <WorkflowDesigner />
          </ReactFlowProvider>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

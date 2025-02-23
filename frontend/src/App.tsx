import React from 'react';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { ReactFlowProvider } from 'reactflow';
import { WorkflowDesigner } from './components/WorkflowDesigner';

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
      <ReactFlowProvider>
        <WorkflowDesigner />
      </ReactFlowProvider>
    </ThemeProvider>
  );
};

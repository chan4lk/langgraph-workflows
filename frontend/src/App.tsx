import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { WorkflowDesigner } from './components/WorkflowDesigner';
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ReactFlowProvider>
        <WorkflowDesigner />
      </ReactFlowProvider>
    </ThemeProvider>
  );
}

export default App;

import React from 'react';
import { Box, AppBar, Toolbar, Typography, Tabs, Tab } from '@mui/material';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

export const MainLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Determine which tab is active based on the current path
  const currentTab = location.pathname.startsWith('/pipelines') ? 1 : 0;

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    if (newValue === 0) {
      navigate('/');
    } else {
      navigate('/pipelines');
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            LangGraph Workflows
          </Typography>
        </Toolbar>
        <Tabs 
          value={currentTab} 
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          sx={{ px: 2 }}
        >
          <Tab label="Workflow Designer" />
          <Tab label="Data Pipelines" />
        </Tabs>
      </AppBar>
      <Box component="main" sx={{ flexGrow: 1, overflow: 'auto' }}>
        <Outlet />
      </Box>
    </Box>
  );
};

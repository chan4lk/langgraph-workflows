import React from 'react';
import { Box, Container, Toolbar, AppBar, Typography, IconButton } from '@mui/material';
import { Outlet, useNavigate } from 'react-router-dom';
import { Dashboard as DashboardIcon } from '@mui/icons-material';

export const PipelineLayout: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="dashboard"
            onClick={() => navigate('/')}
            sx={{ mr: 2 }}
          >
            <DashboardIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            DataPipeline
          </Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flexGrow: 1, overflow: 'auto', py: 3 }}>
        <Outlet />
      </Container>
      <Box component="footer" sx={{ py: 2, textAlign: 'center', borderTop: '1px solid #eaeaea' }}>
        <Typography variant="body2" color="text.secondary">
          © {new Date().getFullYear()} DataPipeline. All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
};

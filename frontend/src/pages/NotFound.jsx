import React from 'react';
import { Box, Container, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Error as ErrorIcon } from '@mui/icons-material';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5',
      }}
    >
      <Container maxWidth="sm" sx={{ textAlign: 'center' }}>
        <ErrorIcon sx={{ fontSize: 80, color: '#ff4d4f', mb: 2 }} />
        <Typography variant="h3" sx={{ fontWeight: 700, mb: 2 }}>
          404
        </Typography>
        <Typography variant="h5" sx={{ mb: 3, color: 'textSecondary' }}>
          Page Not Found
        </Typography>
        <Typography variant="body2" sx={{ mb: 4, color: 'textSecondary' }}>
          The page you're looking for doesn't exist or has been moved.
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button variant="contained" onClick={() => navigate('/dashboard')}>
            Go to Dashboard
          </Button>
          <Button variant="outlined" onClick={() => navigate(-1)}>
            Go Back
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default NotFound;

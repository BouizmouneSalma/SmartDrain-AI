import React from 'react';
import { Box, Typography, Button, Container, Paper } from '@mui/material';
import { Error as ErrorIcon } from '@mui/icons-material';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  reset = () => {
    this.setState({ hasError: false, error: null });
    window.location.href = '/dashboard';
  };

  render() {
    if (this.state.hasError) {
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
          <Container maxWidth="sm">
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <ErrorIcon sx={{ fontSize: 80, color: '#ff4d4f', mb: 2 }} />
              <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                Something went wrong
              </Typography>
              <Typography variant="body2" sx={{ mb: 3, color: 'textSecondary' }}>
                We encountered an unexpected error. Please try again.
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  mb: 3,
                  p: 2,
                  backgroundColor: '#f5f5f5',
                  borderRadius: 1,
                  fontFamily: 'monospace',
                  textAlign: 'left',
                  overflow: 'auto',
                  maxHeight: 200,
                }}
              >
                {this.state.error?.toString()}
              </Typography>
              <Button variant="contained" onClick={this.reset}>
                Return to Dashboard
              </Button>
            </Paper>
          </Container>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

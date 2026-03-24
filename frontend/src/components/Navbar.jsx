import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  Box,
  Container,
  Avatar,
  Tooltip,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
    navigate('/login');
  };

  return (
    <AppBar position="sticky" sx={{ backgroundColor: '#1565c0' }}>
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              cursor: 'pointer',
              mr: 'auto',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            }}
            onClick={() => navigate('/dashboard')}
          >
            🔍 Frouge AI
          </Typography>

          <Box sx={{ display: 'flex', gap: 2, mr: 3 }}>
            <Button
              color="inherit"
              onClick={() => navigate('/dashboard')}
              sx={{ textTransform: 'none', fontSize: '1rem' }}
            >
              Dashboard
            </Button>
            <Button
              color="inherit"
              onClick={() => navigate('/detect')}
              sx={{ textTransform: 'none', fontSize: '1rem' }}
            >
              Detect
            </Button>
            <Button
              color="inherit"
              onClick={() => navigate('/history')}
              sx={{ textTransform: 'none', fontSize: '1rem' }}
            >
              History
            </Button>
          </Box>

          {user && (
            <>
              <Tooltip title={user.email}>
                <Avatar
                  sx={{
                    cursor: 'pointer',
                    backgroundColor: '#42a5f5',
                    width: 40,
                    height: 40,
                  }}
                  onClick={handleMenuOpen}
                >
                  {user.email?.charAt(0).toUpperCase()}
                </Avatar>
              </Tooltip>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem disabled>
                  <Typography variant="body2">{user.email}</Typography>
                </MenuItem>
                <MenuItem onClick={() => { navigate('/profile'); handleMenuClose(); }}>
                  My Profile
                </MenuItem>
                <MenuItem onClick={() => { navigate('/settings'); handleMenuClose(); }}>
                  Settings
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;

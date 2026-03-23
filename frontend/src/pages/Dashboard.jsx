import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
  CircularProgress,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  CloudUpload,
  History as HistoryIcon,
  TrendingUp,
  CheckCircle,
} from '@mui/icons-material';
import { historyAPI } from '../utils/api';
import Navbar from '../components/Navbar';

const Dashboard = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalDetections: 0,
    goodCovers: 0,
    brokenCovers: 0,
    loseCovers: 0,
  });

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await historyAPI.getHistory();
      setHistory(response.data || []);
      
      // Calculate statistics
      const detections = response.data || [];
      const stats = {
        totalDetections: detections.length,
        goodCovers: detections.filter((d) => d.type === 'Good').length,
        brokenCovers: detections.filter((d) => d.type === 'Broken').length,
        loseCovers: detections.filter((d) => d.type === 'Lose').length,
      };
      setStats(stats);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { label: 'Total Detections', value: stats.totalDetections, icon: '📊', color: '#667eea' },
    { label: 'Good Covers', value: stats.goodCovers, icon: '✅', color: '#52c41a' },
    { label: 'Broken Covers', value: stats.brokenCovers, icon: '❌', color: '#ff4d4f' },
    { label: 'Lose Covers', value: stats.loseCovers, icon: '⚠️', color: '#faad14' },
  ];

  return (
    <>
      <Navbar />
      <Box sx={{ backgroundColor: '#f5f5f5', minHeight: '100vh', py: 4 }}>
        <Container maxWidth="lg">
          {/* Header */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
              🔍 Dashboard
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Welcome back! Monitor your cover detection activities
            </Typography>
          </Box>

          {/* Statistics Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            {statCards.map((stat, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card sx={{ height: '100%', borderTop: `4px solid ${stat.color}` }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Box>
                        <Typography color="textSecondary" variant="body2" sx={{ mb: 1 }}>
                          {stat.label}
                        </Typography>
                        <Typography variant="h4" sx={{ fontWeight: 700 }}>
                          {stat.value}
                        </Typography>
                      </Box>
                      <Typography variant="h5">{stat.icon}</Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Action Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 4, textAlign: 'center', cursor: 'pointer', transition: 'all 0.3s', '&:hover': { boxShadow: 4 } }} onClick={() => navigate('/detect')}>
                <CloudUpload sx={{ fontSize: 48, color: '#667eea', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  Upload & Detect
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  Upload an image to detect covers and anomalies
                </Typography>
                <Button variant="contained" size="small">
                  Start Detection
                </Button>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 4, textAlign: 'center', cursor: 'pointer', transition: 'all 0.3s', '&:hover': { boxShadow: 4 } }} onClick={() => navigate('/history')}>
                <HistoryIcon sx={{ fontSize: 48, color: '#52c41a', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  Detection History
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  View all your previous detections and results
                </Typography>
                <Button variant="contained" size="small">
                  View History
                </Button>
              </Paper>
            </Grid>
          </Grid>

          {/* Recent Detections */}
          <Paper sx={{ p: 3, mb: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Recent Detections
              </Typography>
              <Button variant="text" size="small" onClick={() => navigate('/history')}>
                View All →
              </Button>
            </Box>

            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
                <CircularProgress />
              </Box>
            ) : history.length === 0 ? (
              <Box sx={{ py: 3, textAlign: 'center' }}>
                <Typography color="textSecondary">
                  No detections yet. Start by uploading an image!
                </Typography>
              </Box>
            ) : (
              <Box>
                {history.slice(0, 5).map((item, index) => (
                  <Box key={index} sx={{ py: 2, borderBottom: index < 4 ? '1px solid #f0f0f0' : 'none' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {item.filename || `Detection ${index + 1}`}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {item.timestamp || 'Recently'}
                        </Typography>
                      </Box>
                      <Chip label={item.status || 'Completed'} color="primary" size="small" />
                    </Box>
                  </Box>
                ))}
              </Box>
            )}
          </Paper>

          {/* Quick Stats */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
              Detection Accuracy
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2">Overall Confidence</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>95%</Typography>
              </Box>
              <LinearProgress variant="determinate" value={95} sx={{ height: 8, borderRadius: 4 }} />
            </Box>
            <Typography variant="caption" color="textSecondary">
              Based on {stats.totalDetections} detections
            </Typography>
          </Paper>
        </Container>
      </Box>
    </>
  );
};

export default Dashboard;

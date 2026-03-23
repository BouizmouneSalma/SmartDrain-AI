import React, { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Button,
  CircularProgress,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  Grid,
} from '@mui/material';
import { Search, Download, Delete } from '@mui/icons-material';
import { historyAPI } from '../utils/api';
import Navbar from '../components/Navbar';

const History = () => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [stats, setStats] = useState({
    totalDetections: 0,
    successRate: 100,
    avgConfidence: 0,
  });

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    if (searchQuery === '') {
      setFilteredHistory(history);
    } else {
      const filtered = history.filter((item) =>
        JSON.stringify(item).toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredHistory(filtered);
    }
    setPage(0);
  }, [searchQuery, history]);

  const fetchHistory = async () => {
    try {
      const response = await historyAPI.getHistory();
      const historyData = response.data || [];
      setHistory(historyData);
      setFilteredHistory(historyData);

      // Calculate statistics
      if (historyData.length > 0) {
        const completedCount = historyData.filter((h) => h.status === 'Completed').length;
        const successRate = (completedCount / historyData.length * 100).toFixed(1);
        setStats({
          totalDetections: historyData.length,
          successRate,
          avgConfidence: 92.5, // Mock value
        });
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleDelete = async (index) => {
    const updatedHistory = history.filter((_, i) => i !== index);
    setHistory(updatedHistory);
    setFilteredHistory(updatedHistory);
  };

  const handleDownload = () => {
    const dataStr = JSON.stringify(filteredHistory, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `detection_history_${Date.now()}.json`;
    link.click();
  };

  const displayedHistory = filteredHistory.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <>
      <Navbar />
      <Box sx={{ backgroundColor: '#f5f5f5', minHeight: '100vh', py: 4 }}>
        <Container maxWidth="lg">
          {/* Header */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
              📋 Detection History
            </Typography>
            <Typography variant="body2" color="textSecondary">
              View all your detection results and analytics
            </Typography>
          </Box>

          {/* Statistics */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" variant="body2" sx={{ mb: 1 }}>
                    Total Detections
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700 }}>
                    {stats.totalDetections}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" variant="body2" sx={{ mb: 1 }}>
                    Success Rate
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, color: '#52c41a' }}>
                    {stats.successRate}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" variant="body2" sx={{ mb: 1 }}>
                    Avg Confidence
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700 }}>
                    {stats.avgConfidence}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" variant="body2" sx={{ mb: 1 }}>
                    Results
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700 }}>
                    {filteredHistory.length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Search and Actions */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
              <TextField
                placeholder="Search detections..."
                variant="outlined"
                size="small"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Search />
                    </InputAdornment>
                  ),
                }}
                sx={{ minWidth: 300 }}
              />
              <Button
                startIcon={<Download />}
                variant="contained"
                size="small"
                onClick={handleDownload}
                disabled={filteredHistory.length === 0}
              >
                Export
              </Button>
            </Box>
          </Paper>

          {/* History Table */}
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 5 }}>
              <CircularProgress />
            </Box>
          ) : filteredHistory.length === 0 ? (
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" color="textSecondary">
                No detection history found
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Start uploading images to see your detection history
              </Typography>
            </Paper>
          ) : (
            <>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell sx={{ fontWeight: 600 }}>Filename</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Timestamp</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Detections</TableCell>
                      <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600 }}>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {displayedHistory.map((item, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Typography variant="body2">
                            {item.filename || `Detection ${index + 1}`}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" color="textSecondary">
                            {item.timestamp
                              ? new Date(item.timestamp).toLocaleString()
                              : 'Recently'}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {item.detectionCount || 0}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={item.status || 'Completed'}
                            color={item.status === 'Completed' ? 'success' : 'default'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell align="right">
                          <Button
                            startIcon={<Delete />}
                            size="small"
                            variant="text"
                            color="error"
                            onClick={() => handleDelete(index)}
                          >
                            Delete
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                component="div"
                count={filteredHistory.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </>
          )}
        </Container>
      </Box>
    </>
  );
};

export default History;

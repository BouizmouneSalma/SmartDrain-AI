import React, { useState, useCallback } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  LinearProgress,
} from '@mui/material';
import { CloudUpload, Download, Share } from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { predictAPI, historyAPI } from '../utils/api';
import Navbar from '../components/Navbar';

const CLASSES = ['Broken', 'Good', 'Lose', 'Uncovered'];
const CLASS_COLORS = {
  'Broken': '#ff4d4f',
  'Good': '#52c41a',
  'Lose': '#faad14',
  'Uncovered': '#1890ff',
};

const getErrorMessage = (err) => {
  const detail = err?.response?.data?.detail;
  if (typeof detail === 'string') {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item?.msg) return item.msg;
        return 'Validation error';
      })
      .join(', ');
  }
  return 'Detection failed. Please try again.';
};

const Detection = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detections, setDetections] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setSelectedFile(file);
      setError('');
      setSuccess('');

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
    },
  });

  const handleDetect = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await predictAPI.predictImage(selectedFile);
      const detectionData = response.data.detections || [];

      // Format detections
      const formattedDetections = detectionData.map((det) => ({
        class: det.class_name || CLASSES[det.class] || 'Unknown',
        confidence: (det.confidence * 100).toFixed(2),
        bbox: det.bbox,
      }));

      setDetections(formattedDetections);

      // Save to history
      const topType = formattedDetections[0]?.class || 'Uncovered';
      await historyAPI.addHistory({
        filename: selectedFile.name,
        status: 'Completed',
        detectionCount: detectionData.length,
        type: topType,
      });

      setSuccess(`Detection complete! Found ${detectionData.length} object(s)`);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
    setDetections([]);
    setError('');
    setSuccess('');
  };

  const handleDownloadResults = () => {
    const dataStr = JSON.stringify(detections, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `detections_${Date.now()}.json`;
    link.click();
  };

  return (
    <>
      <Navbar />
      <Box sx={{ backgroundColor: '#f5f5f5', minHeight: '100vh', py: 4 }}>
        <Container maxWidth="lg">
          {/* Header */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
              📸 Cover Detection
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Upload an image to detect and classify covers
            </Typography>
          </Box>

          <Grid container spacing={4}>
            {/* Upload Section */}
            <Grid item xs={12} md={6}>
              <Paper
                {...getRootProps()}
                sx={{
                  p: 4,
                  textAlign: 'center',
                  cursor: 'pointer',
                  backgroundColor: isDragActive ? '#e3f2fd' : 'white',
                  borderWidth: 2,
                  borderStyle: 'dashed',
                  borderColor: isDragActive ? '#667eea' : '#d9d9d9',
                  transition: 'all 0.3s',
                  '&:hover': {
                    borderColor: '#667eea',
                    backgroundColor: '#f8f9ff',
                  },
                }}
              >
                <input {...getInputProps()} />
                <CloudUpload sx={{ fontSize: 48, color: '#667eea', mb: 2 }} />
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  {isDragActive ? 'Drop your image here' : 'Drag & drop your image'}
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  or click to select
                </Typography>
                <Button variant="contained" size="small">
                  Choose File
                </Button>
              </Paper>

              {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
              {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}

              {!selectedFile ? (
                <Card sx={{ mt: 3 }}>
                  <CardContent>
                    <Typography variant="body2" color="textSecondary">
                      📝 Supported formats: JPEG, PNG
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Max file size: 25MB
                    </Typography>
                  </CardContent>
                </Card>
              ) : (
                <Box sx={{ mt: 3 }}>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                        Selected File:
                      </Typography>
                      <Typography variant="body2" color="textSecondary" sx={{ wordBreak: 'break-all' }}>
                        {selectedFile.name}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {(selectedFile.size / 1024).toFixed(2)} KB
                      </Typography>
                    </CardContent>
                  </Card>

                  <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Button
                      fullWidth
                      variant="contained"
                      disabled={loading}
                      onClick={handleDetect}
                    >
                      {loading ? <CircularProgress size={24} /> : 'Run Detection'}
                    </Button>
                    <Button
                      fullWidth
                      variant="outlined"
                      disabled={loading}
                      onClick={handleClear}
                    >
                      Clear
                    </Button>
                  </Box>
                </Box>
              )}
            </Grid>

            {/* Preview Section */}
            <Grid item xs={12} md={6}>
              {preview ? (
                <Paper sx={{ p: 2 }}>
                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                    Image Preview
                  </Typography>
                  <Box
                    component="img"
                    src={preview}
                    sx={{
                      width: '100%',
                      borderRadius: 1,
                      maxHeight: 400,
                      objectFit: 'contain',
                    }}
                  />
                </Paper>
              ) : (
                <Paper sx={{ p: 4, textAlign: 'center', height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Typography color="textSecondary">No image selected</Typography>
                </Paper>
              )}
            </Grid>
          </Grid>

          {/* Detections Results */}
          {detections.length > 0 && (
            <Paper sx={{ mt: 4, p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Detection Results
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    startIcon={<Download />}
                    size="small"
                    variant="outlined"
                    onClick={handleDownloadResults}
                  >
                    Download
                  </Button>
                </Box>
              </Box>

              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell sx={{ fontWeight: 600 }}>Class</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600 }}>Confidence</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 600 }}>Bounding Box</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {detections.map((detection, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Chip
                            label={detection.class}
                            sx={{
                              backgroundColor: CLASS_COLORS[detection.class] || '#667eea',
                              color: 'white',
                            }}
                          />
                        </TableCell>
                        <TableCell align="right">
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {detection.confidence}%
                            </Typography>
                            <LinearProgress
                              variant="determinate"
                              value={parseFloat(detection.confidence)}
                              sx={{ mt: 0.5, height: 4, borderRadius: 2 }}
                            />
                          </Box>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="caption">
                            [{detection.bbox.map((v) => v.toFixed(1)).join(', ')}]
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              <Box sx={{ mt: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                  📊 Summary
                </Typography>
                <Grid container spacing={2}>
                  {Object.entries(
                    detections.reduce((acc, det) => {
                      acc[det.class] = (acc[det.class] || 0) + 1;
                      return acc;
                    }, {})
                  ).map(([className, count]) => (
                    <Grid item xs={6} sm={3} key={className}>
                      <Card>
                        <CardContent sx={{ textAlign: 'center', py: 2 }}>
                          <Typography color="textSecondary" variant="caption">
                            {className}
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700 }}>
                            {count}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            </Paper>
          )}
        </Container>
      </Box>
    </>
  );
};

export default Detection;

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  normalizeEmail: (email) => email.trim().toLowerCase(),
  register: (email, password) =>
    api.post('/auth/register', { email: authAPI.normalizeEmail(email), password }),
  login: (email, password) =>
    api.post('/auth/login', { email: authAPI.normalizeEmail(email), password }),
};

export const predictAPI = {
  predictImage: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/predict/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 30000,
    });
  },
  predictVideo: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/predict/video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 300000, // 5 minutes for video processing
    });
  },
};

export const historyAPI = {
  getHistory: () => api.get('/history/'),
  addHistory: (item) => api.post('/history/', item),
};

export default api;

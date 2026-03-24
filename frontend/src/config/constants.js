// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_TIMEOUT = 30000; // 30 seconds

// Cover Detection Classes
export const COVER_CLASSES = {
  BROKEN: 'Broken',
  GOOD: 'Good',
  LOSE: 'Lose',
  UNCOVERED: 'Uncovered',
};

export const CLASS_LABELS = ['Broken', 'Good', 'Lose', 'Uncovered'];

export const CLASS_COLORS = {
  'Broken': '#ff4d4f',
  'Good': '#52c41a',
  'Lose': '#faad14',
  'Uncovered': '#1890ff',
};

// Confidence Thresholds
export const CONFIDENCE_THRESHOLDS = {
  HIGH: 0.8,
  MEDIUM: 0.5,
  LOW: 0.3,
};

// File Upload Configuration
export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: 25 * 1024 * 1024, // 25MB
  ACCEPTED_FORMATS: ['image/jpeg', 'image/png', 'image/webp'],
  ACCEPTED_EXTENSIONS: ['.jpg', '.jpeg', '.png', '.webp'],
};

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 25, 50],
};

// Date/Time Formats
export const DATE_FORMAT = 'YYYY-MM-DD';
export const TIME_FORMAT = 'HH:mm:ss';
export const DATETIME_FORMAT = 'YYYY-MM-DD HH:mm:ss';

// Routes
export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  DETECT: '/detect',
  HISTORY: '/history',
  PROFILE: '/profile',
  NOT_FOUND: '/404',
};

// Local Storage Keys
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
  THEME: 'theme',
  LANGUAGE: 'language',
  PREFERENCES: 'preferences',
};

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
};

// Detection Result Statuses
export const DETECTION_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  FAILED: 'failed',
};

// Notification Messages
export const MESSAGES = {
  LOGIN_SUCCESS: 'Login successful!',
  LOGIN_ERROR: 'Login failed. Please check your credentials.',
  REGISTER_SUCCESS: 'Account created successfully!',
  REGISTER_ERROR: 'Registration failed. Please try again.',
  DETECTION_SUCCESS: 'Detection completed successfully!',
  DETECTION_ERROR: 'Detection failed. Please try again.',
  FILE_UPLOAD_ERROR: 'File upload failed. Please check the file size and format.',
  NETWORK_ERROR: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'Your session has expired. Please log in again.',
};

// Default Pagination
export const DEFAULT_PAGE = 0;
export const DEFAULT_PAGE_SIZE = 10;

export default {
  API_BASE_URL,
  API_TIMEOUT,
  COVER_CLASSES,
  CLASS_LABELS,
  CLASS_COLORS,
  ROUTES,
  STORAGE_KEYS,
  MESSAGES,
};

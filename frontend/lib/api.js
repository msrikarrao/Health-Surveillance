import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api'
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  googleAuth: (googleData) => api.post('/auth/google', googleData)
};

export const reports = {
  submit: (reportData) => api.post('/report', reportData),
  getAll: (params) => api.get('/reports', { params })
};

export const predictions = {
  predict: (village) => api.post('/predict', { village }),
  getAll: (params) => api.get('/predictions', { params })
};

export default api;

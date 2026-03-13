import axios from 'axios';

const API_BASE_URL = 'http://192.168.49.2:30319';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const getCapitals = async () => {
  const response = await api.get('/api/capitals');
  return response.data;
};

export const getCapital = async (id) => {
  const response = await api.get('/api/capitals/${id}');
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
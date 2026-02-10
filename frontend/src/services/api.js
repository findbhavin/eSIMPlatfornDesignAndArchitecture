/**
 * API Service for eSim Platform
 * Handles all API calls to the backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Circuit APIs
export const getCircuits = async () => {
  const response = await api.get('/circuits');
  return response.data;
};

export const getCircuit = async (circuitId) => {
  const response = await api.get(`/circuits/${circuitId}`);
  return response.data;
};

export const analyzeCircuit = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const analyzeCircuitContent = async (content) => {
  const response = await api.post('/analyze', { content });
  return response.data;
};

// Simulation APIs
export const runSimulation = async (circuitId) => {
  const response = await api.post('/simulate', { circuit_id: circuitId });
  return response.data;
};

export const runSimulationWithFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/simulate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getSimulationStatus = async (simId) => {
  const response = await api.get(`/simulation/${simId}/status`);
  return response.data;
};

// Configuration APIs
export const getConfig = async () => {
  const response = await api.get('/config');
  return response.data;
};

export const updateConfig = async (config) => {
  const response = await api.put('/config', config);
  return response.data;
};

// Tools APIs
export const getTools = async () => {
  const response = await api.get('/tools');
  return response.data;
};

export const installTool = async (toolName) => {
  const response = await api.post('/tools/install', { tool_name: toolName });
  return response.data;
};

export default api;

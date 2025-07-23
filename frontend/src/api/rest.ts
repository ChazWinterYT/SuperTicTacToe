import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL ? `${process.env.REACT_APP_API_URL}/api/v1` : 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

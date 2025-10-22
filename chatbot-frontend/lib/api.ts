import axios from 'axios'

// Automatically detect backend URL based on environment
const getApiBaseUrl = () => {
  // Check if environment variable is set (for production)
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL
  }

  // For local development
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    // If accessing from network IP, use same IP for backend
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      return `http://${hostname}:8000`
    }
  }

  // Default to localhost
  return 'http://localhost:8000'
}

const API_BASE_URL = getApiBaseUrl()

console.log('🔗 API Base URL:', API_BASE_URL)

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for LLM responses
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ERR_NETWORK') {
      console.error('❌ Network Error: Backend server may not be running')
      console.error('Expected backend at:', API_BASE_URL)
      console.error('Make sure your FastAPI server is running with:')
      console.error('python -m uvicorn app.main:app --host 0.0.0.0 --port 8000')
    }
    return Promise.reject(error)
  }
)

export default api

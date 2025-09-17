import axios from 'axios'

// Базовая конфигурация API
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptors для обработки токенов и ошибок
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API методы
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
}

export const usersAPI = {
  getAll: () => api.get('/users'),
  create: (userData) => api.post('/users', userData),
}

export const computersAPI = {
  getAll: () => api.get('/computers'),
  create: (computerData) => api.post('/computers', computerData),
  delete: (id) => api.delete(`/computers/${id}`),
}

export const licensesAPI = {
  getAll: (computerId = null) => {
    const params = computerId ? { computer_id: computerId } : {}
    return api.get('/licenses', { params })
  },
  create: (licenseData) => api.post('/licenses', licenseData),
  update: (id, licenseData) => api.put(`/licenses/${id}`, licenseData),
  delete: (id) => api.delete(`/licenses/${id}`),
  search: (filters) => api.get('/licenses/search', { params: filters }),
}

export const mainAPI = {
  getInfo: () => api.get('/'),
}

export default api
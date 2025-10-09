/**
 * API Client Configuration
 * 
 * This demonstrates API integration best practices:
 * - Centralized API configuration
 * - Automatic token handling
 * - Request/Response interceptors
 * - Error handling
 */

import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// Create axios instance
export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          })

          const { access } = response.data
          localStorage.setItem('access_token', access)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/token/', { email, password })
    return response.data
  },
  
  register: async (data: {
    email: string
    password: string
    password_confirm: string
    first_name: string
    last_name: string
  }) => {
    const response = await api.post('/auth/users/', data)
    return response.data
  },
  
  getProfile: async () => {
    const response = await api.get('/auth/users/me/')
    return response.data
  },
  
  updateProfile: async (data: any) => {
    const response = await api.patch('/auth/users/me/', data)
    return response.data
  },
  
  changePassword: async (data: {
    old_password: string
    new_password: string
    new_password_confirm: string
  }) => {
    const response = await api.post('/auth/users/change_password/', data)
    return response.data
  },
}

export const tasksAPI = {
  list: async (params?: any) => {
    const response = await api.get('/tasks/', { params })
    return response.data
  },
  
  get: async (id: number) => {
    const response = await api.get(`/tasks/${id}/`)
    return response.data
  },
  
  create: async (data: any) => {
    const response = await api.post('/tasks/', data)
    return response.data
  },
  
  update: async (id: number, data: any) => {
    const response = await api.patch(`/tasks/${id}/`, data)
    return response.data
  },
  
  delete: async (id: number) => {
    const response = await api.delete(`/tasks/${id}/`)
    return response.data
  },
  
  statistics: async () => {
    const response = await api.get('/tasks/statistics/')
    return response.data
  },
  
  addComment: async (taskId: number, text: string) => {
    const response = await api.post(`/tasks/${taskId}/add_comment/`, { text })
    return response.data
  },
}

export const categoriesAPI = {
  list: async () => {
    const response = await api.get('/tasks/categories/')
    return response.data
  },
  
  create: async (data: any) => {
    const response = await api.post('/tasks/categories/', data)
    return response.data
  },
}

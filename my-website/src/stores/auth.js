import { defineStore } from 'pinia'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('authToken'),
    isAuthenticated: !!localStorage.getItem('authToken'),
    loading: false,
    error: null
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated && !!state.token,
    currentUser: (state) => state.user,
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authAPI.login(credentials)
        
        if (response.data.success) {
          this.user = response.data.data
          this.token = response.data.token || 'mock-token' // Если бэк не возвращает токен
          this.isAuthenticated = true
          
          localStorage.setItem('authToken', this.token)
          localStorage.setItem('user', JSON.stringify(this.user))
          
          return { success: true, data: response.data }
        } else {
          throw new Error(response.data.message || 'Ошибка входа')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Ошибка сети'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authAPI.register(userData)
        
        if (response.data.success) {
          return { success: true, data: response.data }
        } else {
          throw new Error(response.data.message || 'Ошибка регистрации')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Ошибка сети'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      this.error = null
      
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
    },

    initializeAuth() {
      const token = localStorage.getItem('authToken')
      const user = localStorage.getItem('user')
      
      if (token && user) {
        this.token = token
        this.user = JSON.parse(user)
        this.isAuthenticated = true
      }
    }
  }
})

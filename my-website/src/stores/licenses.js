import { defineStore } from 'pinia'
import { licensesAPI } from '@/api'

export const useLicensesStore = defineStore('licenses', {
  state: () => ({
    licenses: [],
    searchResults: [],
    loading: false,
    error: null,
    filters: {
      software: '',
      room: '',
      active_only: false
    }
  }),

  getters: {
    getLicenseById: (state) => (id) => {
      return state.licenses.find(license => license.id === id)
    },
    activeLicenses: (state) => {
      const today = new Date().toISOString().split('T')[0]
      return state.licenses.filter(license => license.license_end >= today)
    },
    expiredLicenses: (state) => {
      const today = new Date().toISOString().split('T')[0]
      return state.licenses.filter(license => license.license_end < today)
    },
    totalBudget: (state) => {
      return state.licenses.reduce((total, license) => total + (license.budget || 0), 0)
    }
  },

  actions: {
    async fetchLicenses(computerId = null) {
      this.loading = true
      this.error = null
      
      try {
        const response = await licensesAPI.getAll(computerId)
        if (response.data.success) {
          this.licenses = response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка загрузки лицензий'
      } finally {
        this.loading = false
      }
    },

    async addLicense(licenseData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await licensesAPI.create(licenseData)
        if (response.data.success) {
          await this.fetchLicenses() // Перезагружаем список
          return { success: true, data: response.data }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка добавления лицензии'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateLicense(id, licenseData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await licensesAPI.update(id, licenseData)
        if (response.data.success) {
          await this.fetchLicenses() // Перезагружаем список
          return { success: true, data: response.data }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка обновления лицензии'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteLicense(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await licensesAPI.delete(id)
        if (response.data.success) {
          this.licenses = this.licenses.filter(license => license.id !== id)
          return { success: true }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка удаления лицензии'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async searchLicenses(filters) {
      this.loading = true
      this.error = null
      this.filters = { ...this.filters, ...filters }
      
      try {
        const response = await licensesAPI.search(this.filters)
        if (response.data.success) {
          this.searchResults = response.data.data
          return { success: true, data: response.data.data }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка поиска лицензий'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    clearSearch() {
      this.searchResults = []
      this.filters = {
        software: '',
        room: '',
        active_only: false
      }
    }
  }
})

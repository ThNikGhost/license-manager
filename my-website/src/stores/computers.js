import { defineStore } from 'pinia'
import { computersAPI } from '@/api'

export const useComputersStore = defineStore('computers', {
  state: () => ({
    computers: [],
    loading: false,
    error: null
  }),

  getters: {
    getComputerById: (state) => (id) => {
      return state.computers.find(computer => computer.id === id)
    },
    sortedComputers: (state) => {
      return [...state.computers].sort((a, b) => a.room_number.localeCompare(b.room_number))
    }
  },

  actions: {
    async fetchComputers() {
      this.loading = true
      this.error = null
      
      try {
        const response = await computersAPI.getAll()
        if (response.data.success) {
          this.computers = response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка загрузки компьютеров'
      } finally {
        this.loading = false
      }
    },

    async addComputer(computerData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await computersAPI.create(computerData)
        if (response.data.success) {
          await this.fetchComputers() // Перезагружаем список
          return { success: true, data: response.data }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка добавления компьютера'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteComputer(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await computersAPI.delete(id)
        if (response.data.success) {
          this.computers = this.computers.filter(computer => computer.id !== id)
          return { success: true }
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Ошибка удаления компьютера'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    }
  }
})

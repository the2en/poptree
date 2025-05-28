import { defineStore } from 'pinia'
import axios from 'axios'

export const useSpendingStore = defineStore('spending', {
  state: () => ({
    spendingData: null,
    categories: [],
    aiFeedback: '',
    loading: false,
    error: null
  }),

  actions: {
    async fetchSpendingAnalysis() {
      this.loading = true
      try {
        const response = await axios.get('/api/spending/analysis/')
        this.spendingData = response.data
        this.categories = response.data.categories
        this.aiFeedback = response.data.aiFeedback
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateSpendingCategory(categoryId, data) {
      try {
        const response = await axios.patch(`/api/spending/categories/${categoryId}/`, data)
        const index = this.categories.findIndex(c => c.id === categoryId)
        if (index !== -1) {
          this.categories[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    }
  },

  getters: {
    totalSpending: (state) => {
      if (!state.spendingData) return 0
      return state.spendingData.amounts.reduce((sum, amount) => sum + amount, 0)
    },

    categoryTotals: (state) => {
      return state.categories.reduce((acc, category) => {
        acc[category.name] = category.total
        return acc
      }, {})
    }
  }
}) 
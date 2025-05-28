import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const useInvestmentStore = defineStore('investment', {
  state: () => ({
    products: [],
    marketData: [],
    recommendedProducts: [],
    selectedProduct: null,
    searchFilters: {
      query: '',
      type: '',
      minRate: null,
      maxRate: null
    },
    loading: false,
    error: null
  }),

  actions: {
    async searchProducts(filters = {}) {
      this.loading = true
      try {
        const params = new URLSearchParams()
        if (filters.query) params.append('q', filters.query)
        if (filters.type) params.append('type', filters.type)
        if (filters.minRate) params.append('min_rate', filters.minRate)
        if (filters.maxRate) params.append('max_rate', filters.maxRate)

        const response = await axios.get(`/api/investments/products/search/?${params}`)
        this.products = response.data.products
        this.searchFilters = filters
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchProductDetail(productId) {
      this.loading = true
      try {
        const response = await axios.get(`/api/investments/products/${productId}/`)
        this.selectedProduct = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchRecommendedProducts() {
      this.loading = true
      try {
        const response = await axios.get('/api/investments/products/recommended/')
        this.recommendedProducts = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    clearFilters() {
      this.searchFilters = {
        query: '',
        type: '',
        minRate: null,
        maxRate: null
      }
    },

    async fetchProducts() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/api/investments/products/list/`)
        this.products = response.data
        return response.data
      } catch (error) {
        console.error('투자 상품 목록 요청 실패:', error)
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchMarketData() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/api/investments/market/list/`)
        this.marketData = response.data
        return response.data
      } catch (error) {
        console.error('ETF 시장 데이터 요청 실패:', error)
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    }
  },

  getters: {
    filteredProducts: (state) => {
      return state.products
    },

    productCount: (state) => {
      return state.products.length
    },

    hasActiveFilters: (state) => {
      return Object.values(state.searchFilters).some(value => value !== '' && value !== null)
    }
  }
}) 
// frontend/stores/commune.js

import { defineStore } from 'pinia'
import axios from 'axios'

export const useCommuneStore = defineStore('commune', {
  state: () => ({
    communes: [],
    isLoading: false,
    error: null,
  }),
  
  getters: {
    getCommuneById: (state) => (id) => {
      return state.communes.find(commune => commune.id === id) || null
    },
    
    getCommuneOptions: (state) => {
      return state.communes.map(commune => ({
        value: commune.id,
        label: commune.nom
      }))
    }
  },
  
  actions: {
    async fetchCommunes() {
      try {
        this.isLoading = true
        this.error = null
        
        const config = useRuntimeConfig()
        const response = await axios.get(`${config.public.apiBaseUrl}/communes/`)
        
        this.communes = response.data
        return this.communes
      } catch (error) {
        this.error = error.response?.data || 'Erreur lors de la récupération des communes'
        throw error
      } finally {
        this.isLoading = false
      }
    }
  }
})
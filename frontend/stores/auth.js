import { defineStore } from 'pinia'
import jwtDecode from 'jwt-decode'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    refreshToken: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
  },

  actions: {
    async register(userData) {
      try {
        this.isLoading = true
        this.error = null

        const config = useRuntimeConfig()
        const response = await axios.post(`${config.public.apiBaseUrl}/accounts/register/`, userData)

        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Erreur lors de l\'inscription'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async verifyEmail(verificationData) {
      try {
        this.isLoading = true
        this.error = null

        const config = useRuntimeConfig()
        const response = await axios.post(`${config.public.apiBaseUrl}/accounts/verify-email/`, verificationData)

        this.setAuthData(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Erreur lors de la vérification de l\'email'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async login(credentials) {
      try {
        this.isLoading = true
        this.error = null

        const config = useRuntimeConfig()
        const response = await axios.post(`${config.public.apiBaseUrl}/accounts/login/`, credentials)

        this.setAuthData(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Erreur lors de la connexion'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      try {
        this.isLoading = true

        if (this.refreshToken) {
          const config = useRuntimeConfig()
          await axios.post(
            `${config.public.apiBaseUrl}/accounts/logout/`,
            { refresh: this.refreshToken },
            { headers: { Authorization: `Bearer ${this.token}` } }
          )
        }

        this.clearAuthData()
        return { success: true }
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
        this.clearAuthData()
        return { success: true }
      } finally {
        this.isLoading = false
      }
    },

    async fetchCurrentUser() {
      try {
        if (!this.token) return null

        this.isLoading = true
        const config = useRuntimeConfig()
        const response = await axios.get(
          `${config.public.apiBaseUrl}/accounts/me/`,
          { headers: { Authorization: `Bearer ${this.token}` } }
        )

        this.user = response.data
        return this.user
      } catch (error) {
        console.error('Erreur lors de la récupération du profil:', error)
        if (error.response?.status === 401) {
          this.clearAuthData()
        }
        return null
      } finally {
        this.isLoading = false
      }
    },

    setAuthData(data) {
      this.token = data.access
      this.refreshToken = data.refresh
      this.user = data.user

      // Enregistrer dans le localStorage uniquement côté client
      if (process.client) {
        localStorage.setItem('auth_token', this.token)
        localStorage.setItem('auth_refresh', this.refreshToken)
        localStorage.setItem('auth_user', JSON.stringify(this.user))
      }

      this.setupAxiosInterceptor()
    },

    clearAuthData() {
      this.user = null
      this.token = null
      this.refreshToken = null

      // Supprimer du localStorage uniquement côté client
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_refresh')
        localStorage.removeItem('auth_user')
      }
    },

    initAuth() {
      // Cette méthode ne doit s'exécuter que côté client
      if (!process.client) return false

      const token = localStorage.getItem('auth_token')
      const refresh = localStorage.getItem('auth_refresh')
      const user = JSON.parse(localStorage.getItem('auth_user') || 'null')

      if (token && refresh && user) {
        try {
          const decoded = jwtDecode(token)
          const currentTime = Date.now() / 1000

          if (decoded.exp > currentTime) {
            this.token = token
            this.refreshToken = refresh
            this.user = user
            this.setupAxiosInterceptor()
            return true
          }
        } catch (error) {
          console.error('Erreur lors du décodage du token:', error)
        }
      }

      this.clearAuthData()
      return false
    },

    setupAxiosInterceptor() {
      axios.interceptors.request.use(
        (config) => {
          if (this.token) {
            config.headers.Authorization = `Bearer ${this.token}`
          }
          return config
        },
        (error) => Promise.reject(error)
      )
    }
  }
})

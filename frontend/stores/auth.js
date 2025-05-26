import { defineStore } from 'pinia';
import axios from 'axios';

// Créer une instance axios avec la configuration de base
const apiClient = axios.create({
  baseURL: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    loading: false,
    error: null,
    isAuthenticated: false
  }),

  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    getLoading: (state) => state.loading,
    getError: (state) => state.error,
    getIsAuthenticated: (state) => state.isAuthenticated
  },

  actions: {
    // Inscription
    async register(userData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await apiClient.post('/api/accounts/register/', userData);
        return response.data;
      } catch (error) {
        this.error = error.response?.data || "Une erreur s'est produite lors de l'inscription";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Connexion
    async login(credentials) {
      this.loading = true;
      this.error = null;

      try {
        const response = await apiClient.post('/api/accounts/login/', credentials);
        const { token } = response.data;

        this.token = token;
        this.isAuthenticated = true;

        if (process.client) {
          localStorage.setItem('authToken', token.access);
        }

        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.access}`;
        await this.fetchUserProfile();

        return response.data;
      } catch (error) {
        this.error = error.response?.data || "Une erreur s'est produite lors de la connexion";
        throw error;
      } finally {
        this.loading = false;
      }
    },


    // Vérification du compte
    async verifyAccount(verificationData) {
      this.loading = true;
      this.error = null;

      try {
        const response = await apiClient.post('/api/accounts/verify/', verificationData);
        return response.data;
      } catch (error) {
        this.error = error.response?.data || "Une erreur s'est produite lors de la vérification du compte";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Déconnexion
    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;

      if (process.client) {
        localStorage.removeItem('authToken');
      }

      delete apiClient.defaults.headers.common['Authorization'];
    },

    // Initialiser l'authentification
    initAuth() {
      if (process.client) {
        const accessToken = localStorage.getItem('authToken');
        if (accessToken) {
          this.token = { access: accessToken }; // simule structure de login
          this.isAuthenticated = true;

          // Assure-toi que l'en-tête est bien mis
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

          // Puis appelle le profil
          this.fetchUserProfile();
        }
      }
    },

  // Renvoi du code de vérification
  async resendVerificationCode(email) {
    this.loading = true;
    this.error = null;

    try {
      const response = await apiClient.post('/api/accounts/resend-code/', { email });
      return response.data;
    } catch (error) {
      this.error = error.response?.data || "Erreur lors du renvoi du code";
      throw error;
    } finally {
      this.loading = false;
    }
  },
    // Récupérer le mot de passe


    // Récupérer le profil utilisateur
    async fetchUserProfile() {
      if (!this.token) return;
      this.loading = true;

      try {
        const response = await apiClient.get('/api/accounts/me/');
        this.user = response.data;
      } catch (error) {
        if (error.response?.status === 401) {
          this.logout();
        }
      } finally {
        this.loading = false;
      }
    }
  }
});

// Service pour les communes
export const useCommunes = () => {
  const getCommunes = async () => {
    try {
      const response = await apiClient.get('/api/communes/');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des communes:', error);
      throw error;
    }
  };

  return { getCommunes };
};

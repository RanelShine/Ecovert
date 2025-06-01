import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import type { Commune } from '~/types'

// Fonction utilitaire pour obtenir le token
const getAuthToken = (): string => {
    // Essayer d'abord dans le localStorage
    let token = localStorage.getItem('authToken')
    if (!token) {
        // Essayer dans le sessionStorage
        token = sessionStorage.getItem('authToken')
    }
    if (!token) {
        // Essayer de récupérer depuis les cookies
        const cookieToken = document.cookie
            .split('; ')
            .find(row => row.startsWith('authToken='))
            ?.split('=')[1]
        if (cookieToken) {
            token = cookieToken
        }
    }
    return token || ''
}

// Configuration de l'instance axios
const apiClient = axios.create({
    baseURL: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})

interface State {
    communes: Commune[];
    isLoading: boolean;
    error: string | null;
}

export const useCommuneStore = defineStore('commune', {
    state: (): State => ({
        communes: [],
        isLoading: false,
        error: null,
    }),

    getters: {
        getCommuneById: (state): ((id: number) => Commune | null) => {
            return (id: number) => state.communes.find(commune => commune.id === id) || null
        },

        getCommuneOptions: (state) => {
            return state.communes.map(commune => ({
                value: commune.id,
                label: commune.nom
            }))
        },

        // Getter pour les communes avec coordonnées valides
        getCommunesWithCoordinates: (state): Commune[] => {
            return state.communes.filter(commune =>
                typeof commune.latitude === 'number' &&
                typeof commune.longitude === 'number' &&
                commune.latitude !== null &&
                commune.longitude !== null
            )
        },

        // Getter pour obtenir les régions uniques
        getRegions: (state): string[] => {
            const regions = new Set(state.communes.map(c => c.region))
            return Array.from(regions)
        }
    },

    actions: {
        async fetchCommunes() {
            const router = useRouter()
            try {
                this.isLoading = true
                this.error = null

                // Vérifier si l'utilisateur est authentifié
                const token = getAuthToken()
                console.log('[DEBUG] Token récupéré:', token ? 'Présent' : 'Absent')

                if (!token) {
                    console.log('[DEBUG] Pas de token trouvé, redirection vers login')
                    const currentPath = window.location.pathname
                    router.push(`/auth/login?redirect=${encodeURIComponent(currentPath)}`)
                    throw new Error('Non authentifié')
                }

                // Configurer le token pour la requête
                console.log('[DEBUG] Configuration du token pour la requête')
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`

                console.log('[DEBUG] Envoi de la requête GET /api/communes/')
                const response = await apiClient.get('/api/communes/', {
                    params: {
                        has_coordinates: true
                    }
                })

                console.log('[DEBUG] Réponse reçue:', {
                    status: response.status,
                    hasData: !!response.data,
                    resultsLength: response.data?.results?.length
                })

                if (response.data && response.data.results) {
                    // Vérifier et nettoyer les données des communes
                    this.communes = response.data.results.map((commune: any): Commune => ({
                        ...commune,
                        latitude: commune.latitude ? parseFloat(commune.latitude) : null,
                        longitude: commune.longitude ? parseFloat(commune.longitude) : null
                    }))

                    console.log('[DEBUG] Communes chargées:', {
                        total: this.communes.length,
                        withCoordinates: this.communes.filter(c =>
                            typeof c.latitude === 'number' &&
                            typeof c.longitude === 'number' &&
                            c.latitude !== null &&
                            c.longitude !== null
                        ).length
                    })
                } else {
                    console.warn('[DEBUG] Format de réponse inattendu:', response.data)
                    this.communes = []
                }

                return this.communes
            } catch (error: any) {
                console.error('[DEBUG] Erreur détaillée:', {
                    message: error.message,
                    response: error.response?.data,
                    status: error.response?.status,
                    headers: error.response?.headers
                })

                if (error.response?.status === 401) {
                    console.log('[DEBUG] Erreur 401 détectée, redirection vers login')
                    const currentPath = window.location.pathname
                    router.push(`/auth/login?redirect=${encodeURIComponent(currentPath)}`)
                }

                this.error = error.response?.data?.message ||
                    error.response?.data ||
                    error.message ||
                    'Erreur lors de la récupération des communes'

                this.communes = []
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // Nouvelle action pour rechercher des communes
        async searchCommunes(searchTerm: string): Promise<Commune[]> {
            try {
                const token = getAuthToken()
                if (!token) throw new Error('Non authentifié')

                apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`

                const response = await apiClient.get('/api/communes/', {
                    params: {
                        search: searchTerm
                    }
                })
                return response.data.results || []
            } catch (error) {
                console.error('Erreur lors de la recherche des communes:', error)
                throw error
            }
        },

        // Nouvelle action pour obtenir les communes par région
        async getCommunesByRegion(region: string): Promise<Commune[]> {
            try {
                const token = getAuthToken()
                if (!token) throw new Error('Non authentifié')

                apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`

                const response = await apiClient.get('/api/communes/', {
                    params: {
                        region: region
                    }
                })
                return response.data.results || []
            } catch (error) {
                console.error('Erreur lors de la récupération des communes par région:', error)
                throw error
            }
        },

        // Réinitialiser le store
        reset() {
            this.communes = []
            this.isLoading = false
            this.error = null
        }
    },

    // Persistance du store (optionnel)
    persist: {
        storage: localStorage,
        paths: ['communes']
    }
}) 
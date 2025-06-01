<!-- MapSection.vue -->
<template>
    <div class="map-container">
        <!-- En-tête avec statistiques -->
        <div class="bg-white p-4 rounded-lg shadow mb-4">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-2xl font-semibold text-green-700">Carte des Signalements</h2>
                <div class="flex gap-4 text-sm">
                    <div class="bg-red-100 px-3 py-1 rounded">
                        <span class="text-red-700 font-medium">{{ stats.pollution }}</span>
                        <span class="text-red-600 ml-1">Pollution</span>
                    </div>
                    <div class="bg-yellow-100 px-3 py-1 rounded">
                        <span class="text-yellow-700 font-medium">{{ stats.dechets }}</span>
                        <span class="text-yellow-600 ml-1">Déchets</span>
                    </div>
                    <div class="bg-blue-100 px-3 py-1 rounded">
                        <span class="text-blue-700 font-medium">{{ stats.climat }}</span>
                        <span class="text-blue-600 ml-1">Climat</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Filtres améliorés -->
        <div class="filters bg-white p-4 rounded-lg shadow mb-4">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <!-- Filtre par type avec couleurs -->
                <div class="filter-group">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Type de signalement</label>
                    <select v-model="selectedType" @change="updateFilters" class="w-full border rounded-md p-2">
                        <option value="">Tous les types</option>
                        <option v-for="type in typeChoices" :key="type.value" :value="type.value">
                            {{ type.label }}
                        </option>
                    </select>
                </div>

                <!-- Filtre par commune (limité selon le rôle CTD) -->
                <div class="filter-group">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Commune</label>
                    <select v-model="selectedCommune" @change="updateFilters" class="w-full border rounded-md p-2">
                        <option value="">Toutes les communes</option>
                        <option v-for="commune in availableCommunes" :key="commune.id" :value="commune.id">
                            {{ commune.nom }}
                        </option>
                    </select>
                </div>

                <!-- Filtre par statut -->
                <div class="filter-group">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Statut</label>
                    <select v-model="selectedStatus" @change="updateFilters" class="w-full border rounded-md p-2">
                        <option value="">Non traités</option>
                        <option value="en_attente">En attente</option>
                        <option value="en_cours">En cours</option>
                    </select>
                </div>

                <!-- Actions -->
                <div class="filter-group flex items-end">
                    <div class="w-full space-y-2">
                        <button @click="resetFilters"
                            class="w-full bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
                            Réinitialiser
                        </button>
                        <button @click="refreshSignalements"
                            class="w-full bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                            Actualiser
                        </button>
                        <!-- Bouton pour activer la géolocalisation -->
                        <button @click="getUserLocation"
                            class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                            Ma position
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Légende des couleurs -->
        <div class="bg-white p-4 rounded-lg shadow mb-4">
            <h3 class="text-sm font-medium text-gray-700 mb-2">Légende</h3>
            <div class="flex flex-wrap gap-4 text-sm">
                <div class="flex items-center">
                    <div class="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
                    <span>Pollution</span>
                </div>
                <div class="flex items-center">
                    <div class="w-4 h-4 bg-yellow-500 rounded-full mr-2"></div>
                    <span>Déchets</span>
                </div>
                <div class="flex items-center">
                    <div class="w-4 h-4 bg-blue-500 rounded-full mr-2"></div>
                    <span>Climat</span>
                </div>
                <div class="flex items-center">
                    <div class="w-3 h-3 border-2 border-green-600 rounded-full mr-2"></div>
                    <span>Ma position {{ userPosition ? '(activée)' : '(désactivée)' }}</span>
                </div>
            </div>
        </div>

        <!-- Messages de debug -->
        <div v-if="debugMode" class="bg-yellow-100 p-4 rounded-lg shadow mb-4">
            <h3 class="text-sm font-bold text-yellow-800 mb-2">Debug Info</h3>
            <div class="text-xs text-yellow-700 space-y-1">
                <p>Position utilisateur: {{ debugInfo.userPosition }}</p>
                <p>Total signalements chargés: {{ debugInfo.totalSignalements }}</p>
                <p>Signalements avec coordonnées valides: {{ debugInfo.validCoordinates }}</p>
                <p>Signalements filtrés: {{ debugInfo.filteredCount }}</p>
                <p>Marqueurs affichés sur la carte: {{ debugInfo.markersCount }}</p>
                <div v-if="debugInfo.totalSignalements > 0 && debugInfo.validCoordinates === 0"
                    class="bg-red-100 p-2 rounded mt-2">
                    <p class="text-red-700 font-medium">⚠️ Aucun signalement n'a de coordonnées GPS valides!</p>
                    <p class="text-red-600 text-xs">Vérifiez votre API photo et les données de latitude/longitude.</p>
                </div>
            </div>
            <button @click="debugMode = false" class="mt-2 text-xs bg-yellow-200 px-2 py-1 rounded hover:bg-yellow-300">
                Masquer Debug
            </button>
            <button @click="loadSignalements" class="mt-2 ml-2 text-xs bg-blue-200 px-2 py-1 rounded hover:bg-blue-300">
                Recharger Data
            </button>
        </div>

        <!-- Bouton de debug flottant -->
        <button v-if="!debugMode" @click="debugMode = true"
            class="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded text-xs z-20">
            Debug
        </button>

        <!-- Carte avec limites Cameroun -->
        <div class="map-wrapper bg-white rounded-lg shadow overflow-hidden" style="height: 600px;">
            <ClientOnly>
                <l-map ref="map" v-model:zoom="zoom" v-model:center="center" :use-global-leaflet="false"
                    :options="mapOptions" :max-bounds="camerounBounds" @ready="onMapReady">

                    <!-- Couche de tuiles OpenStreetMap -->
                    <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" :attribution="attribution"
                        :options="tileLayerOptions" />

                    <!-- Si l'utilisateur est CTD, afficher les limites de sa commune -->
                    <l-rectangle v-if="userRole === 'ctd' && mapBounds" :bounds="mapBounds" :options="{
                        color: '#047857',
                        weight: 2,
                        fillColor: '#047857',
                        fillOpacity: 0.1
                    }" />

                    <!-- Marqueur de position utilisateur -->
                    <l-marker v-if="userPosition" :lat-lng="userPosition" :icon="userLocationIcon">
                        <l-popup>
                            <div class="text-center">
                                <p class="font-medium">Votre position</p>
                                <p class="text-xs text-gray-600">{{ userPosition[0].toFixed(4) }}, {{
                                    userPosition[1].toFixed(4) }}</p>
                            </div>
                        </l-popup>
                    </l-marker>

                    <!-- Marqueurs des signalements avec validation des coordonnées -->
                    <l-marker v-for="marker in validMarkers" :key="marker.id" :lat-lng="marker.coordinates"
                        :icon="getMarkerIcon(marker.signalement.type_signalement)"
                        @click="showSignalementDetails(marker.signalement)">

                        <l-popup :options="{ maxWidth: 300, className: 'custom-popup' }">
                            <div class="popup-content">
                                <h3 class="font-semibold mb-2 text-gray-800">{{ marker.signalement.objet }}</h3>

                                <div class="mb-2">
                                    <span class="inline-block px-2 py-1 rounded text-xs font-medium"
                                        :class="getTypeClass(marker.signalement.type_signalement)">
                                        {{ marker.signalement.type_signalement_display }}
                                    </span>
                                    <span class="inline-block px-2 py-1 rounded text-xs font-medium ml-1"
                                        :class="statusClass(marker.signalement.statut)">
                                        {{ marker.signalement.statut_display }}
                                    </span>
                                </div>

                                <p class="text-sm text-gray-600 mb-2 line-clamp-2">
                                    {{ marker.signalement.description }}
                                </p>

                                <!-- Image depuis votre API photo -->
                                <div v-if="marker.signalement.photos && marker.signalement.photos.length > 0"
                                    class="mb-3">
                                    <img :src="marker.signalement.photos[0].image_url || marker.signalement.photos[0].url"
                                        :alt="marker.signalement.objet" class="w-full h-24 object-cover rounded"
                                        loading="lazy" @error="handleImageError($event)" />
                                </div>

                                <div class="text-xs text-gray-500 mb-3">
                                    <p>📍 {{ marker.signalement.localisation }}</p>
                                    <p>📅 {{ formatDate(marker.signalement.date_signalement) }}</p>
                                    <p v-if="marker.signalement.commune">🏛️ {{ marker.signalement.commune.nom }}</p>
                                    <p class="text-yellow-600">🔗 {{ marker.coordinates[0].toFixed(6) }}, {{
                                        marker.coordinates[1].toFixed(6) }}</p>
                                    <p v-if="marker.signalement.photos?.[0]?.date_uploaded" class="text-blue-600">
                                        📷 Photo: {{ formatDate(marker.signalement.photos[0].date_uploaded) }}
                                    </p>
                                </div>

                                <div class="flex justify-between items-center">
                                    <button @click="showSignalementDetails(marker.signalement)"
                                        class="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600">
                                        Détails
                                    </button>
                                    <button @click="openGoogleMapsDirections(marker.signalement)"
                                        class="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600">
                                        Itinéraire
                                    </button>
                                </div>
                            </div>
                        </l-popup>
                    </l-marker>

                    <!-- Cercles des communes avec popups améliorés -->
                    <l-circle v-for="commune in communesWithBounds" :key="commune.id"
                        :lat-lng="[commune.latitude, commune.longitude]" :radius="commune.radius" :options="{
                            color: commune.id.toString() === selectedCommune ? '#047857' : '#10B981',
                            weight: 2,
                            opacity: commune.id.toString() === selectedCommune ? 0.8 : 0.3,
                            fillOpacity: commune.id.toString() === selectedCommune ? 0.2 : 0.1
                        }">
                        <l-popup>
                            <div class="p-3">
                                <h3 class="font-semibold text-lg text-gray-800 mb-2">{{ commune.nom }}</h3>
                                <div class="text-sm text-gray-600">
                                    <p>🏛️ Région: {{ commune.region }}</p>
                                    <p>📍 Coordonnées: {{ commune.latitude.toFixed(4) }}, {{
                                        commune.longitude.toFixed(4) }}</p>
                                    <p>⭕ Rayon: {{ (commune.radius / 1000).toFixed(1) }} km</p>
                                </div>
                                <button @click="selectedCommune = commune.id.toString()"
                                    class="mt-3 bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600">
                                    Filtrer les signalements
                                </button>
                            </div>
                        </l-popup>
                    </l-circle>
                </l-map>
            </ClientOnly>

            <!-- Indicateur de chargement -->
            <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-10">
                <div class="flex items-center space-x-2">
                    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-green-600"></div>
                    <span class="text-gray-600">Chargement des signalements...</span>
                </div>
            </div>
        </div>

        <!-- Modal détails du signalement amélioré -->
        <div v-if="selectedSignalement"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            @click.self="selectedSignalement = null">
            <div class="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
                <div class="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
                    <h2 class="text-xl font-semibold text-gray-800">{{ selectedSignalement.objet }}</h2>
                    <button @click="selectedSignalement = null" class="text-gray-500 hover:text-gray-700 text-2xl">
                        &times;
                    </button>
                </div>

                <div class="p-6 space-y-6">
                    <!-- Photo principale -->
                    <div v-if="selectedSignalement.photos && selectedSignalement.photos.length > 0"
                        class="aspect-video w-full">
                        <img :src="selectedSignalement.photos[0].image_url" :alt="selectedSignalement.objet"
                            class="w-full h-full object-cover rounded-lg" />
                    </div>

                    <!-- Informations principales -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-4">
                            <div>
                                <h3 class="font-medium text-gray-700 mb-2">Type et Statut</h3>
                                <div class="space-y-2">
                                    <span class="inline-block px-3 py-1 rounded-full text-sm font-medium"
                                        :class="getTypeClass(selectedSignalement.type_signalement)">
                                        {{ selectedSignalement.type_signalement_display }}
                                    </span>
                                    <span class="inline-block px-3 py-1 rounded-full text-sm font-medium ml-2"
                                        :class="statusClass(selectedSignalement.statut)">
                                        {{ selectedSignalement.statut_display }}
                                    </span>
                                </div>
                            </div>

                            <div>
                                <h3 class="font-medium text-gray-700 mb-2">Localisation</h3>
                                <p class="text-gray-600">{{ selectedSignalement.localisation }}</p>
                                <p v-if="selectedSignalement.commune" class="text-sm text-gray-500">
                                    Commune: {{ selectedSignalement.commune.nom }}
                                </p>
                            </div>

                            <div>
                                <h3 class="font-medium text-gray-700 mb-2">Signalé par</h3>
                                <p class="text-gray-600">{{ selectedSignalement.utilisateur_nom || 'Anonyme' }}</p>
                            </div>
                        </div>

                        <div class="space-y-4">
                            <div>
                                <h3 class="font-medium text-gray-700 mb-2">Date de signalement</h3>
                                <p class="text-gray-600">{{ formatDate(selectedSignalement.date_signalement) }}</p>
                            </div>

                            <div v-if="selectedSignalement.date_resolution">
                                <h3 class="font-medium text-gray-700 mb-2">Date de résolution</h3>
                                <p class="text-gray-600">{{ formatDate(selectedSignalement.date_resolution) }}</p>
                            </div>

                            <div v-if="getDistanceToSignalement(selectedSignalement)">
                                <h3 class="font-medium text-gray-700 mb-2">Distance</h3>
                                <p class="text-gray-600">{{ getDistanceToSignalement(selectedSignalement) }} km</p>
                            </div>
                        </div>
                    </div>

                    <!-- Description complète -->
                    <div>
                        <h3 class="font-medium text-gray-700 mb-2">Description</h3>
                        <p class="text-gray-600 leading-relaxed">{{ selectedSignalement.description }}</p>
                    </div>

                    <!-- Actions -->
                    <div class="flex flex-wrap gap-3 pt-4 border-t">
                        <button @click="openGoogleMapsDirections(selectedSignalement)"
                            class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 flex items-center gap-2">
                            <span>🗺️</span>
                            Obtenir l'itinéraire
                        </button>

                        <button v-if="canChangeStatus" @click="showStatusChangeModal(selectedSignalement)"
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center gap-2">
                            <span>⚡</span>
                            Changer le statut
                        </button>

                        <button @click="shareSignalement(selectedSignalement)"
                            class="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 flex items-center gap-2">
                            <span>📤</span>
                            Partager
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import 'leaflet/dist/leaflet.css'
import type { Store } from 'pinia'
import { useCommuneStore } from '@/stores/communes'
import axios from 'axios'

// État
const route = useRoute()
const map = ref(null)
const zoom = ref(12)
const center = ref([5.4826, 10.4147]) // Bafoussam par défaut
const selectedType = ref('')
const selectedCommune = ref('')
const selectedStatus = ref('')
const selectedSignalement = ref<Signalement | null>(null)
const signalements = ref<Signalement[]>([])
const communes = ref<Commune[]>([])
const userPosition = ref<[number, number] | null>(null)
const loading = ref(false)
const userRole = ref('')
const canChangeStatus = ref(false)
const debugMode = ref(false)

// Choix de types avec couleurs
const typeChoices = [
    { value: 'pollution', label: 'Pollution', color: '#EF4444' },
    { value: 'dechets', label: 'Déchets', color: '#F59E0B' },
    { value: 'climat', label: 'Climat', color: '#3B82F6' }
]

// Configuration des endpoints API
const API_CONFIG = {
    baseUrl: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
    endpoints: {
        signalements: '/api/signalements/liste/',
        signalementDetail: (id: number) => `/api/signalements/detail/${id}/`,
        photos: '/api/photos',
        communes: '/api/communes/',
        auth: '/api/accounts/me/'
    }
}

// Configuration spécifique au Cameroun
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

// Limites du Cameroun (approximatives)
const camerounBounds = [
    [1.5, 8.0],   // Sud-Ouest
    [13.0, 16.5]  // Nord-Est
]

// État pour les limites de la carte
const mapBounds = ref<number[][] | null>(null)

// Interface pour les communes
interface Commune {
    id: number;
    nom: string;
    region: string;
    latitude: number | null;
    longitude: number | null;
    created_at: string;
    updated_at: string;
}

// Interface pour les communes avec coordonnées validées
interface CommuneWithBounds extends Commune {
    latitude: number;
    longitude: number;
    radius: number;
}

interface Photo {
    id: number
    image_url: string
    url?: string // URL alternative pour l'image
    latitude: number | string | null
    longitude: number | string | null
    date_uploaded: string
}

interface Signalement {
    id: number
    objet: string
    description: string
    type_signalement: string
    type_signalement_display: string
    statut: string
    statut_display: string
    localisation: string
    photos: Photo[]
    date_signalement: string
    date_resolution?: string
    commune?: Commune
    utilisateur_nom?: string
}

// Interface pour le store des communes (mise à jour)
interface CommuneStore extends Store {
    communes: Commune[];
    isLoading: boolean;
    error: string | null;
    fetchCommunes: () => Promise<void>;
}

// Options de la carte mises à jour
const mapOptions = computed(() => ({
    zoomControl: true,
    scrollWheelZoom: true,
    maxZoom: 18,
    minZoom: 12, // Zoom minimum augmenté pour garder le focus sur la commune
    worldCopyJump: false,
    maxBounds: mapBounds.value || camerounBounds,
    maxBoundsViscosity: 1.0, // Force le respect des limites
    doubleClickZoom: false // Désactive le zoom par double-clic
}))

const tileLayerOptions = {
    maxZoom: 18,
    minZoom: 8,
    tileSize: 256,
    zoomOffset: 0,
    detectRetina: true
}

// Fonction utilitaire pour construire les URLs d'API
const buildApiUrl = (endpoint: string, params?: URLSearchParams): string => {
    const base = API_CONFIG.baseUrl
    const url = new URL(endpoint, base)

    if (params) {
        url.search = params.toString()
    }

    if (debugMode.value) {
        console.log('URL API construite:', url.toString(), {
            baseUrl: base,
            endpoint,
            params: params?.toString()
        })
    }

    return url.toString()
}

// Fonction améliorée pour obtenir le token
const getAuthToken = (): string => {
    // Essayer d'abord dans le localStorage
    let token = localStorage.getItem('authToken')
    if (!token) {
        // Essayer dans le sessionStorage
        token = sessionStorage.getItem('authToken')
    }
    if (!token) {
        // Essayer de récupérer depuis les cookies avec gestion du undefined
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

// Interface pour les données utilisateur
interface UserData {
    id: number
    email: string
    nom: string
    prenom: string
    telephone: string
    role: string
    commune: number
    is_active: boolean
    is_verified: boolean
}

// État utilisateur avec composition API
const userData = ref<UserData | null>(null)
const userCommune = ref<number | null>(null)

// Fonction pour charger les données utilisateur depuis l'API
const loadUserData = async () => {
    try {
        if (debugMode.value) {
            console.log('Chargement des données utilisateur...')
        }

        const token = getAuthToken()
        const axiosInstance = axios.create({
            baseURL: API_CONFIG.baseUrl,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })

        const response = await axiosInstance.get(API_CONFIG.endpoints.auth)
        const data = response.data
        userData.value = data
        userRole.value = data.role
        userCommune.value = data.commune

        return data
    } catch (error) {
        console.error('Erreur lors du chargement des données utilisateur:', error)
        throw error
    }
}

// Fonction pour vérifier si l'utilisateur est authentifié
const checkAuth = async () => {
    const token = getAuthToken()
    console.log('[DEBUG] checkAuth - Token:', token ? 'Présent' : 'Absent')

    if (!token) {
        console.log('[DEBUG] checkAuth - Aucun token trouvé')
        clearUserData()
        navigateTo('/auth/login?redirect=' + encodeURIComponent(window.location.pathname))
        return false
    }

    try {
        console.log('[DEBUG] checkAuth - Tentative de chargement des données utilisateur')
        await loadUserData()
        console.log('[DEBUG] checkAuth - Données utilisateur chargées avec succès')
        return true
    } catch (error) {
        console.error('[DEBUG] checkAuth - Erreur:', error)
        clearUserData()
        navigateTo('/auth/login?redirect=' + encodeURIComponent(window.location.pathname))
        return false
    }
}

// Fonction pour nettoyer les données utilisateur
const clearUserData = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userData')
    sessionStorage.removeItem('authToken')
    userData.value = null
    userRole.value = ''
    userCommune.value = null
}

// Fonction pour rafraîchir le token si nécessaire
const refreshToken = async () => {
    try {
        const refreshUrl = buildApiUrl('/accounts/token/refresh/')
        const response = await fetch(refreshUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                refresh: localStorage.getItem('refreshToken')
            })
        })

        if (response.ok) {
            const data = await response.json()
            localStorage.setItem('authToken', data.access)
            return true
        }
        return false
    } catch (error) {
        console.error('Erreur lors du rafraîchissement du token:', error)
        return false
    }
}

// Fonction utilitaire améliorée pour les appels API
const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    if (!checkAuth()) {
        throw new Error('Non authentifié')
    }

    const token = getAuthToken()
    const defaultOptions: RequestInit = {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    }

    try {
        const response = await fetch(endpoint, { ...defaultOptions, ...options })

        if (debugMode.value) {
            console.log('Appel API:', {
                endpoint,
                status: response.status,
                ok: response.ok
            })
        }

        if (response.status === 401) {
            // Token expiré, essayer de le rafraîchir
            if (await refreshToken()) {
                // Réessayer l'appel avec le nouveau token
                const newToken = getAuthToken()
                const newOptions = {
                    ...options,
                    headers: {
                        ...defaultOptions.headers,
                        'Authorization': `Bearer ${newToken}`
                    }
                }
                const retryResponse = await fetch(endpoint, newOptions)
                if (retryResponse.ok) {
                    return retryResponse.json()
                }
            }
            // Si le rafraîchissement échoue, rediriger vers la connexion
            navigateTo('/auth/login?redirect=' + encodeURIComponent(window.location.pathname))
            throw new Error('Session expirée')
        }

        if (!response.ok) {
            const errorText = await response.text()
            console.error('Erreur API:', {
                endpoint,
                status: response.status,
                statusText: response.statusText,
                error: errorText
            })
            throw new Error(`${response.status}: ${response.statusText}`)
        }

        return response.json()
    } catch (error) {
        if (error instanceof Error) {
            throw error
        }
        throw new Error('Erreur réseau')
    }
}

// Fonction pour gérer les erreurs de chargement d'images
const handleImageError = (event: Event) => {
    const img = event.target as HTMLImageElement
    // Image par défaut ou placeholder
    img.src = '/images/placeholder-signalement.jpg'
    console.warn('Erreur chargement image:', img.src)
}

// Statistiques calculées
const stats = computed(() => {
    return {
        pollution: filteredSignalements.value.filter(s => s.type_signalement === 'pollution').length,
        dechets: filteredSignalements.value.filter(s => s.type_signalement === 'dechets').length,
        climat: filteredSignalements.value.filter(s => s.type_signalement === 'climat').length
    }
})

// Communes disponibles selon le rôle
const availableCommunes = computed(() => {
    if (userRole.value === 'ctd') {
        // CTD ne voit que sa commune
        return communes.value.filter(c => c.id === getCurrentUserCommune())
    }
    return communes.value
})

// Communes avec coordonnées pour affichage
const communesWithBounds = computed(() => {
    return communes.value
        .filter((commune): commune is CommuneWithBounds => {
            return typeof commune.latitude === 'number' &&
                typeof commune.longitude === 'number' &&
                commune.latitude !== null &&
                commune.longitude !== null;
        })
        .map(commune => ({
            ...commune,
            radius: 10000 // Rayon par défaut en mètres
        }));
})

// Signalements filtrés avec vérification des coordonnées
const filteredSignalements = computed(() => {
    return signalements.value
        .filter(s => {
            if (!signalementHasValidCoordinates(s)) {
                if (debugMode.value) {
                    console.warn(`Signalement ${s.id} sans coordonnées GPS valides:`, {
                        photos: s.photos?.length || 0,
                        lat: s.photos?.[0]?.latitude,
                        lng: s.photos?.[0]?.longitude
                    })
                }
                return false
            }

            const typeMatch = !selectedType.value || s.type_signalement === selectedType.value
            const communeMatch = !selectedCommune.value || (s.commune?.id === Number(selectedCommune.value))
            const statusMatch = !selectedStatus.value || s.statut === selectedStatus.value ||
                (selectedStatus.value === '' && ['en_cours', 'en_attente'].includes(s.statut))

            // CTD ne voit que les signalements de sa commune
            if (userRole.value === 'ctd' && userCommune.value) {
                return typeMatch && statusMatch && (s.commune?.id === userCommune.value)
            }

            return typeMatch && communeMatch && statusMatch
        })
})

const validMarkers = computed(() => {
    return filteredSignalements.value
        .map(signalement => {
            const coordinates = getSignalementCoordinates(signalement)
            if (!coordinates) return null

            return {
                id: signalement.id,
                coordinates,
                signalement
            }
        })
        .filter((marker): marker is NonNullable<typeof marker> => marker !== null)
})

// Fonctions utilitaires pour les coordonnées
const parseCoordinate = (coord: string | number | null | undefined): number | null => {
    if (coord === null || coord === undefined || coord === '') {
        return null;
    }
    const parsed = parseFloat(String(coord));
    return isNaN(parsed) ? null : parsed;
}

const hasValidCoordinates = (photo: Photo): boolean => {
    if (!photo) return false;

    const lat = parseCoordinate(photo.latitude);
    const lng = parseCoordinate(photo.longitude);

    if (debugMode.value) {
        console.log('Validation coordonnées photo:', {
            photoId: photo.id,
            rawLat: photo.latitude,
            rawLng: photo.longitude,
            parsedLat: lat,
            parsedLng: lng,
            isValid: lat !== null && lng !== null &&
                lat >= -90 && lat <= 90 &&
                lng >= -180 && lng <= 180
        });
    }

    return lat !== null && lng !== null &&
        lat >= -90 && lat <= 90 &&
        lng >= -180 && lng <= 180;
}

const signalementHasValidCoordinates = (signalement: Signalement): boolean => {
    if (!signalement.photos || signalement.photos.length === 0) {
        if (debugMode.value) {
            console.log(`Signalement ${signalement.id} sans photos`);
        }
        return false;
    }

    const hasValid = signalement.photos.some(hasValidCoordinates);

    if (debugMode.value && !hasValid) {
        console.log(`Signalement ${signalement.id} coordonnées invalides:`, {
            nbPhotos: signalement.photos.length,
            photos: signalement.photos.map(p => ({
                id: p.id,
                lat: p.latitude,
                lng: p.longitude
            }))
        });
    }

    return hasValid;
}

const getSignalementCoordinates = (signalement: Signalement): [number, number] | null => {
    if (!signalement.photos || signalement.photos.length === 0) return null;

    // Chercher la première photo avec des coordonnées valides
    const validPhoto = signalement.photos.find(hasValidCoordinates);
    if (!validPhoto) return null;

    const lat = parseCoordinate(validPhoto.latitude);
    const lng = parseCoordinate(validPhoto.longitude);

    if (lat === null || lng === null) return null;

    if (debugMode.value) {
        console.log(`Coordonnées extraites pour signalement ${signalement.id}:`, { lat, lng });
    }

    return [lat, lng];
}

// Mise à jour de la fonction de traitement des photos
const processPhoto = async (photo: Photo, axiosInstance: any): Promise<Photo> => {
    try {
        // Si la photo a déjà des coordonnées valides, on la retourne telle quelle
        if (hasValidCoordinates(photo)) {
            return photo;
        }

        // Sinon, on essaie de récupérer les coordonnées depuis l'API
        const photoResponse = await axiosInstance.get(`${API_CONFIG.endpoints.photos}/${photo.id}`);
        const photoData = photoResponse.data;

        // Vérifier si les coordonnées reçues sont valides
        const updatedPhoto = {
            ...photo,
            latitude: photoData.latitude ?? photo.latitude,
            longitude: photoData.longitude ?? photo.longitude,
            image_url: photoData.image_url || photo.image_url || photo.url
        };

        if (debugMode.value) {
            console.log(`Mise à jour photo ${photo.id}:`, {
                avant: { lat: photo.latitude, lng: photo.longitude },
                après: { lat: updatedPhoto.latitude, lng: updatedPhoto.longitude }
            });
        }

        return updatedPhoto;
    } catch (error) {
        console.warn(`Erreur lors du chargement de la photo ${photo.id}:`, error);
        return photo;
    }
}

// Fonctions utilitaires
const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const statusClass = (status: string) => {
    switch (status) {
        case 'en_cours': return 'bg-yellow-100 text-yellow-800'
        case 'en_attente': return 'bg-red-100 text-red-800'
        case 'traite': return 'bg-green-100 text-green-800'
        default: return 'bg-gray-100 text-gray-800'
    }
}

const getTypeClass = (type: string) => {
    switch (type) {
        case 'pollution': return 'bg-red-100 text-red-800'
        case 'dechets': return 'bg-yellow-100 text-yellow-800'
        case 'climat': return 'bg-blue-100 text-blue-800'
        default: return 'bg-gray-100 text-gray-800'
    }
}

const getMarkerIcon = (type: string) => {
    const typeConfig = typeChoices.find(t => t.value === type)
    const color = typeConfig?.color || '#6B7280'

    return {
        iconUrl: `data:image/svg+xml;base64,${btoa(`
            <svg width="25" height="41" viewBox="0 0 25 41" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.5 0C5.6 0 0 5.6 0 12.5c0 12.2 12.5 28.5 12.5 28.5S25 24.7 25 12.5C25 5.6 19.4 0 12.5 0z" fill="${color}"/>
                <circle cx="12.5" cy="12.5" r="6" fill="white"/>
            </svg>
        `)}`,
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [0, -41]
    }
}

const userLocationIcon = {
    iconUrl: `data:image/svg+xml;base64,${btoa(`
        <svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <circle cx="10" cy="10" r="8" fill="#10B981" stroke="white" stroke-width="2"/>
            <circle cx="10" cy="10" r="3" fill="white"/>
        </svg>
    `)}`,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
}

// Actions
const updateFilters = () => {
    // Déclenché automatiquement par les computed
}

const resetFilters = () => {
    selectedType.value = ''
    selectedCommune.value = ''
    selectedStatus.value = ''
}

const refreshSignalements = async () => {
    await loadSignalements()
}

const getUserLocation = async () => {
    try {
        loading.value = true
        const position = await getCurrentPosition()
        userPosition.value = [position.coords.latitude, position.coords.longitude]
        center.value = userPosition.value
        zoom.value = 15
        console.log('Position utilisateur obtenue:', userPosition.value)
    } catch (error) {
        console.error('Erreur géolocalisation:', error)
        alert('Impossible d\'obtenir votre position. Veuillez activer la géolocalisation dans votre navigateur.')
    } finally {
        loading.value = false
    }
}

const showSignalementDetails = async (signalement: Signalement) => {
    try {
        loading.value = true;
        const axiosInstance = axios.create({
            baseURL: API_CONFIG.baseUrl,
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            }
        });

        const response = await axiosInstance.get(API_CONFIG.endpoints.signalementDetail(signalement.id));

        // S'assurer que les photos ont les bonnes URLs
        if (response.data.photos && response.data.photos.length > 0) {
            response.data.photos = response.data.photos.map((photo: Photo) => ({
                ...photo,
                image_url: photo.image_url || photo.url || '/images/placeholder-signalement.jpg'
            }));
        }

        selectedSignalement.value = response.data;

        if (debugMode.value) {
            console.log('Détails du signalement chargés:', response.data);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des détails du signalement:', error);
        // En cas d'erreur, on utilise les données de base du signalement
        selectedSignalement.value = {
            ...signalement,
            photos: signalement.photos?.map(photo => ({
                ...photo,
                image_url: photo.image_url || photo.url || '/images/placeholder-signalement.jpg'
            }))
        };
        handleError(error as Error, 'data_loading', 'Impossible de charger tous les détails du signalement.');
    } finally {
        loading.value = false;
    }
}

const openGoogleMapsDirections = async (signalement: Signalement) => {
    const coordinates = getSignalementCoordinates(signalement)
    if (!coordinates) {
        alert('Coordonnées GPS non disponibles pour ce signalement.')
        return
    }

    if (!userPosition.value) {
        try {
            const position = await getCurrentPosition()
            userPosition.value = [position.coords.latitude, position.coords.longitude]
        } catch (error) {
            alert('Impossible d\'obtenir votre position. Veuillez activer la géolocalisation.')
            return
        }
    }

    const [userLat, userLng] = userPosition.value
    const [destLat, destLng] = coordinates
    const url = `https://www.google.com/maps/dir/?api=1&origin=${userLat},${userLng}&destination=${destLat},${destLng}&travelmode=driving`
    window.open(url, '_blank')
}

const shareSignalement = (signalement: Signalement) => {
    if (navigator.share) {
        navigator.share({
            title: `Signalement: ${signalement.objet}`,
            text: signalement.description,
            url: window.location.href
        })
    } else {
        // Fallback pour navigateurs non compatibles
        const url = `${window.location.origin}/signalement/${signalement.id}`
        navigator.clipboard.writeText(url).then(() => {
            alert('Lien copié dans le presse-papiers')
        })
    }
}

const showStatusChangeModal = (signalement: Signalement) => {
    // Cette fonction sera implémentée plus tard pour gérer le changement de statut
    console.log('Changement de statut pour le signalement:', signalement.id)
}

const getDistanceToSignalement = (signalement: Signalement) => {
    if (!userPosition.value) return null

    const coordinates = getSignalementCoordinates(signalement)
    if (!coordinates) return null

    const [userLat, userLng] = userPosition.value
    const [signalementLat, signalementLng] = coordinates

    const distance = calculateDistance(userLat, userLng, signalementLat, signalementLng)
    return distance.toFixed(1)
}

const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371 // Rayon de la Terre en km
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLon = (lon2 - lon1) * Math.PI / 180
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
}

const getCurrentPosition = (): Promise<GeolocationPosition> => {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Géolocalisation non supportée'))
            return
        }

        navigator.geolocation.getCurrentPosition(
            resolve,
            reject,
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutes
            }
        )
    })
}

const getCurrentUserCommune = (): number | null => {
    // Cette fonction devra être adaptée selon votre système d'authentification
    // Pour l'exemple, on retourne null
    // Vous devrez implémenter la logique pour récupérer la commune de l'utilisateur connecté
    return null
}

// Fonctions de chargement des données
const loadSignalements = async () => {
    try {
        if (!checkAuth()) {
            return;
        }

        loading.value = true;
        if (debugMode.value) {
            console.log('Début du chargement des signalements...');
        }

        // Construction des paramètres
        const params = new URLSearchParams();
        if (selectedType.value) params.append('type', selectedType.value);
        if (selectedCommune.value) params.append('commune', selectedCommune.value);
        if (selectedStatus.value) params.append('statut', selectedStatus.value);

        // Utilisation d'axios directement
        const axiosInstance = axios.create({
            baseURL: API_CONFIG.baseUrl,
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            }
        });

        if (debugMode.value) {
            console.log('Requête signalements:', {
                url: `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.signalements}`,
                params: Object.fromEntries(params),
                headers: axiosInstance.defaults.headers
            });
        }

        const response = await axiosInstance.get(API_CONFIG.endpoints.signalements, { params });

        if (debugMode.value) {
            console.log('Réponse brute de l\'API:', response.data);
        }

        // Vérification et traitement de la réponse
        if (!response.data) {
            throw new Error('Réponse API vide');
        }

        // Extraction des signalements selon le format de la réponse
        let loadedSignalements: Signalement[] = [];
        if (Array.isArray(response.data)) {
            loadedSignalements = response.data;
        } else if (response.data.results && Array.isArray(response.data.results)) {
            loadedSignalements = response.data.results;
        } else if (typeof response.data === 'object') {
            // Si c'est un objet unique, on le met dans un tableau
            loadedSignalements = [response.data];
        }

        if (debugMode.value) {
            console.log('Signalements extraits:', {
                nombre: loadedSignalements.length,
                premier: loadedSignalements[0] ? {
                    id: loadedSignalements[0].id,
                    photos: loadedSignalements[0].photos?.length || 0
                } : null
            });
        }

        // Traitement des photos pour chaque signalement
        const processedSignalements = await Promise.all(
            loadedSignalements.map(async (signalement: Signalement) => {
                if (!signalement.photos) {
                    signalement.photos = [];
                    return signalement;
                }

                const processedPhotos = await Promise.all(
                    signalement.photos.map(photo => processPhoto(photo, axiosInstance))
                );

                return {
                    ...signalement,
                    photos: processedPhotos
                };
            })
        );

        signalements.value = processedSignalements;

        if (debugMode.value) {
            const validCount = signalements.value.filter(s => signalementHasValidCoordinates(s)).length;
            console.log('Résumé final:', {
                total: signalements.value.length,
                valides: validCount,
                filtres: {
                    type: selectedType.value || 'tous',
                    commune: selectedCommune.value || 'toutes',
                    statut: selectedStatus.value || 'tous'
                }
            });
        }

    } catch (error) {
        console.error('Erreur lors du chargement des signalements:', error);
        signalements.value = [];

        let errorMessage = 'Erreur lors du chargement des données.';
        if (error instanceof Error) {
            errorMessage = `${errorMessage} Détails: ${error.message}`;
        }

        handleError(error as Error, 'data_loading', errorMessage);
    } finally {
        loading.value = false;
    }
};

// Fonction pour calculer les limites d'une commune
const calculateCommuneBounds = (commune: Commune): number[][] | null => {
    if (!commune?.latitude || !commune?.longitude) return null

    const lat = parseFloat(String(commune.latitude))
    const lng = parseFloat(String(commune.longitude))

    // Créer une zone de 10km autour du centre de la commune
    const offset = 0.1 // environ 10km en degrés
    return [
        [lat - offset, lng - offset], // Sud-Ouest
        [lat + offset, lng + offset]  // Nord-Est
    ]
}

// Fonction pour charger les communes améliorée
const loadCommunes = async () => {
    try {
        console.log('[DEBUG] loadCommunes - Début du chargement')

        const communeStore = useCommuneStore()
        console.log('[DEBUG] loadCommunes - Store initialisé')

        await (communeStore as unknown as { fetchCommunes: () => Promise<void> }).fetchCommunes()
        console.log('[DEBUG] loadCommunes - Communes récupérées du store')

        // Si l'utilisateur est CTD, ne garder que sa commune
        if (userRole.value === 'ctd' && userCommune.value) {
            console.log('[DEBUG] loadCommunes - Filtrage pour CTD:', userCommune.value)
            const filteredCommunes = (communeStore.communes as Commune[]).filter(c => c.id === userCommune.value)
            communes.value = filteredCommunes

            // Définir les limites de la carte pour la commune
            const userCommuneData = filteredCommunes[0]
            if (userCommuneData?.latitude && userCommuneData?.longitude) {
                const bounds = calculateCommuneBounds(userCommuneData)
                if (bounds) {
                    mapBounds.value = bounds
                    center.value = [userCommuneData.latitude, userCommuneData.longitude]
                    zoom.value = 14
                }
            }
        } else {
            console.log('[DEBUG] loadCommunes - Chargement de toutes les communes')
            communes.value = communeStore.communes as Commune[]
        }

        console.log('[DEBUG] loadCommunes - Résultat:', {
            total: communes.value.length,
            bounds: mapBounds.value,
            userRole: userRole.value,
            userCommune: userCommune.value
        })

        return communes.value
    } catch (error: any) {
        console.error('[DEBUG] loadCommunes - Erreur:', error)
        communes.value = []
        handleError(error as Error, 'data_loading', 'Impossible de charger la liste des communes.')
    }
}

const loadUserProfile = async () => {
    try {
        const data = await loadUserData()
        canChangeStatus.value = ['admin', 'ctd', 'moderateur'].includes(data.role)

        // Si l'utilisateur est CTD, centrer la carte sur sa commune
        if (data.role === 'ctd' && data.commune) {
            const communeData = communes.value.find(c => c.id === data.commune)
            if (communeData?.latitude && communeData?.longitude) {
                center.value = [communeData.latitude, communeData.longitude]
                zoom.value = 13
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement du profil utilisateur:', error)
        handleError(error as Error, 'data_loading', 'Impossible de charger le profil utilisateur.')
    }
}

// Gestionnaires d'événements de la carte
const onMapReady = () => {
    console.log('Carte initialisée')

    // Centrer la carte sur la première commune disponible si l'utilisateur est CTD
    if (userRole.value === 'ctd' && communesWithBounds.value.length > 0) {
        const commune = communesWithBounds.value[0]
        center.value = [commune.latitude, commune.longitude]
        zoom.value = 13
    }
}

// Watchers pour réactivité
watch([selectedType, selectedCommune, selectedStatus], () => {
    loadSignalements()
}, { deep: true })

watch(userPosition, (newPosition) => {
    if (newPosition) {
        console.log('Position utilisateur mise à jour:', newPosition)
        // Optionnel: centrer la carte sur la nouvelle position
        // center.value = newPosition
    }
})

// Surveiller les changements de route pour recharger les données
watch(route, async (newRoute) => {
    if (debugMode.value) {
        console.log('Changement de route détecté, rechargement des données...', {
            path: newRoute.path,
            query: newRoute.query
        });
    }
    await loadSignalements();
}, { deep: true });

// Lifecycle hooks
onMounted(async () => {
    console.log('[DEBUG] MapSection - Montage du composant')

    if (!checkAuth()) {
        console.log('[DEBUG] MapSection - Échec de l\'authentification')
        return
    }

    console.log('[DEBUG] MapSection - Début du chargement des données')
    // Charger les données initiales
    try {
        await Promise.all([
            loadUserProfile(),
            loadCommunes()
        ])
        console.log('[DEBUG] MapSection - Données initiales chargées')

        // Charger les signalements après avoir chargé le profil utilisateur
        await loadSignalements()
        console.log('[DEBUG] MapSection - Signalements chargés')

    } catch (error) {
        console.error('[DEBUG] MapSection - Erreur lors du chargement initial:', error)
    }

    // Tenter d'obtenir la position utilisateur automatiquement
    try {
        await getUserLocation()
        console.log('[DEBUG] MapSection - Position utilisateur obtenue')
    } catch (error) {
        console.log('[DEBUG] MapSection - Position utilisateur non disponible')
    }
})

// Fonctions exportées pour les tests ou usage externe
const exportedFunctions = {
    loadSignalements,
    refreshSignalements,
    getUserLocation,
    resetFilters,
    formatDate,
    calculateDistance
}

// Gestion des erreurs globales
const handleError = (error: Error, context: string, customMessage?: string) => {
    console.error(`Erreur dans ${context}:`, error)

    if (debugMode.value) {
        console.error('Stack trace:', error.stack)
        console.error('Context:', context)
    }

    const errorMessages: { [key: string]: string } = {
        'geolocation': 'Impossible d\'obtenir votre position. Vérifiez les paramètres de géolocalisation.',
        'data_loading': customMessage || 'Erreur lors du chargement des données. Veuillez réessayer.',
        'map_initialization': 'Erreur lors de l\'initialisation de la carte.',
        'api_call': 'Erreur de communication avec le serveur.'
    }

    const message = errorMessages[context] || 'Une erreur inattendue s\'est produite.'

    if (process.env.NODE_ENV === 'development' || debugMode.value) {
        alert(`[DEBUG] ${message}\n\nDétails: ${error.message}`)
    } else {
        alert(message)
    }
}

// Gestion des événements de visibilité de la page
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Rafraîchir les données quand l'utilisateur revient sur la page
        loadSignalements()
    }
})

// Nettoyage lors de la destruction du composant
onUnmounted(() => {
    // Nettoyer les listeners si nécessaire
    document.removeEventListener('visibilitychange', () => { })
})

// Messages de debug améliorés
const debugInfo = computed(() => {
    const totalSignalements = signalements.value.length
    const validCoordinates = signalements.value.filter(s => signalementHasValidCoordinates(s)).length
    const filteredCount = filteredSignalements.value.length
    const markersCount = validMarkers.value.length

    return {
        totalSignalements,
        validCoordinates,
        filteredCount,
        markersCount,
        userPosition: userPosition.value ?
            `${userPosition.value[0].toFixed(4)}, ${userPosition.value[1].toFixed(4)}` :
            'Non disponible'
    }
})
</script>

<style scoped>
.map-container {
    position: relative;
}

.map-wrapper {
    position: relative;
    z-index: 1;
}

.custom-popup .leaflet-popup-content-wrapper {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.custom-popup .leaflet-popup-content {
    margin: 8px 12px;
    min-width: 200px;
}

.custom-popup .leaflet-popup-tip {
    background: white;
}

/* Animation de pulsation pour le marqueur de position */
@keyframes pulse {
    0% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.2);
        opacity: 0.8;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.pulse-animation {
    animation: pulse 2s infinite;
}

/* Augmenter la taille de la carte */
.map-wrapper {
    height: 70vh !important;
    min-height: 600px;
}
</style>
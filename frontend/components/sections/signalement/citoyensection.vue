<!-- section citoyensection -->
<template>
  <!-- Formulaire de création -->
  <div class="bg-white rounded-lg shadow p-4 sm:p-6 mb-6 sm:mb-8 dark:bg-gray-600 mx-2 sm:mx-0">
    <h2 class="text-xl sm:text-2xl lg:text-3xl text-center font-semibold text-green-700 mb-4 sm:mb-6 dark:text-green-600">
      Faire un signalement
    </h2>

    <!-- Boutons de type - Responsive -->
    <div class="flex flex-wrap gap-2 mb-4 sm:mb-6 justify-center sm:justify-start">
      <button
        v-for="type in typeChoices"
        :key="type.value"
        @click="selectedType = type.value"
        :class="[
          'px-3 py-2 sm:px-4 sm:py-2 rounded shadow capitalize text-sm sm:text-base flex-1 sm:flex-none min-w-0',
          selectedType === type.value
            ? 'bg-green-700 text-white'
            : 'bg-green-100 text-green-800 hover:bg-green-200'
        ]"
      >
        {{ type.label }}
      </button>
    </div>

    <!-- Champs du formulaire -->
    <div class="space-y-4 mb-4 sm:mb-6">
      <!-- Objet et Localisation -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <input 
          v-model="objet" 
          type="text" 
          placeholder="Objet du signalement" 
          class="border rounded-lg p-3 w-full text-sm sm:text-base focus:ring-2 focus:ring-green-500 focus:border-transparent" 
          required
        />
        <input 
          v-model="localisation" 
          type="text" 
          placeholder="Localisation" 
          class="border rounded-lg p-3 w-full text-sm sm:text-base focus:ring-2 focus:ring-green-500 focus:border-transparent" 
          required
        />
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Géolocalisation -->
      <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg"> 
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Latitude
            </label>
            <input 
              v-model="latitude" 
              type="number" 
              step="any"
              placeholder="Ex: 5.4734" 
              :disabled="useAutoLocation"
              :class="[
                'border rounded-lg p-3 w-full text-sm sm:text-base focus:ring-2 focus:ring-green-500 focus:border-transparent',
                useAutoLocation 
                  ? 'bg-gray-100 dark:bg-gray-600 cursor-not-allowed' 
                  : 'bg-white dark:bg-gray-800'
              ]"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Longitude
            </label>
            <input 
              v-model="longitude" 
              type="number" 
              step="any"
              placeholder="Ex: 10.4181" 
              :disabled="useAutoLocation"
              :class="[
                'border rounded-lg p-3 w-full text-sm sm:text-base focus:ring-2 focus:ring-green-500 focus:border-transparent',
                useAutoLocation 
                  ? 'bg-gray-100 dark:bg-gray-600 cursor-not-allowed' 
                  : 'bg-white dark:bg-gray-800'
              ]"
              required
            />
          </div>
           <div class="fgrid grid-cols-1 sm:grid-cols-2 gap-4">
            <label
            class="inline-flex items-center px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg cursor-pointer transition-colors duration-300"
            :class="useAutoLocation ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-300'"
          >
            <input
              type="checkbox"
              v-model="useAutoLocation"
              @change="toggleAutoLocation"
              class="hidden"
            />
            <span class="text-sm font-medium">
              {{ useAutoLocation ? 'Auto activé' : 'Auto désactivé' }}
            </span>
          </label>
        </div>
        </div>
        
        <!-- Indicateur de géolocalisation -->
        <div v-if="locationStatus" class="mt-3 p-2 rounded-lg text-sm">
          <div v-if="locationStatus === 'loading'" class="text-blue-600 bg-blue-50 p-2 rounded">
            Récupération de votre position...
          </div>
          <div v-else-if="locationStatus === 'success'" class="text-green-600 bg-green-50 p-2 rounded">
            Position obtenue automatiquement
          </div>
          <div v-else-if="locationStatus === 'error'" class="text-red-600 bg-red-50 p-2 rounded">
            ❌ {{ locationError }}
          </div>
        </div>
      </div>

      <!-- Description -->
      <textarea 
        v-model="description" 
        placeholder="Description détaillée du problème" 
        class="border rounded-lg p-3 w-full h-24 sm:h-28 text-sm sm:text-base resize-none focus:ring-2 focus:ring-green-500 focus:border-transparent" 
        required
      ></textarea>
        </div>
      
      <!-- Upload de fichier et caméra -->
      <div class="space-y-4">
        <div class="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
          <div class="flex-1">
            <input
              type="file"
              accept="image/*"
              @change="onFileChange"
              class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
            />
          </div>
          <button 
            @click="openCameraModal" 
            class="bg-green-600 text-white px-4 py-2 sm:px-6 sm:py-3 rounded-lg shadow hover:bg-green-700 transition-colors text-sm sm:text-base whitespace-nowrap"
          >
            Prendre une photo
          </button>
        </div>

        <!-- Aperçu de la photo sélectionnée -->
        <div v-if="file || photoPreview" class="bg-green-50 dark:bg-green-900 p-4 rounded-lg border border-green-200 dark:border-green-700">
          <div class="flex items-start gap-4">
            <!-- Aperçu de l'image -->
            <div v-if="photoPreview" class="flex-shrink-0">
              <div class="relative">
                <img 
                  :src="photoPreview" 
                  alt="Aperçu de la photo" 
                  class="w-20 h-20 sm:w-24 sm:h-24 object-cover rounded-lg border-2 border-green-300 shadow-sm"
                />
                <button 
                  @click="removePhoto"
                  class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600 transition-colors shadow-lg"
                  title="Supprimer la photo"
                >
                  ✕
                </button>
              </div>
            </div>
            
            <!-- Informations sur le fichier -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span class="text-sm font-medium text-green-700 dark:text-green-300">Photo sélectionnée</span>
              </div>
              <p class="text-sm text-green-600 dark:text-green-400 truncate">
                {{ file?.name || 'Photo capturée' }}
              </p>
              <p class="text-xs text-green-500 dark:text-green-500 mt-1">
                {{ formatFileSize(file?.size) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

<!-- Bouton de soumission -->
<div class="flex justify-end mt-4">
  <button
    @click="submitSignalement"
    :disabled="loading || !objet || !localisation || !description || !file || !latitude || !longitude"
    :class="[
      'w-fit px-4 py-2 sm:py-3 rounded-lg shadow text-sm sm:text-base font-semibold transition-colors',
      loading || !objet || !localisation || !description || !file || !latitude || !longitude
        ? 'bg-gray-400 cursor-not-allowed text-gray-600'
        : 'bg-green-700 hover:bg-green-800 text-white'
    ]"
  >
    {{ loading ? 'Envoi en cours...' : 'Envoyer le signalement' }}
  </button>
</div>

  </div>

  <!-- Mes signalements -->
  <div class="bg-white rounded-lg shadow mx-2 sm:mx-0 dark:bg-gray-600">
    <div class="bg-green-600 text-white p-4 sm:p-6 font-semibold rounded-t-lg">
      <h3 class="text-lg sm:text-xl">Mes signalements ({{ mesSignalements.length }})</h3>
    </div>
    
    <div class="p-4 sm:p-6 bg-gray-50 dark:bg-gray-600">
      <!-- Version mobile - Cards -->
      <div class="block sm:hidden space-y-4">
        <div 
          v-for="s in mesSignalements" 
          :key="s.id" 
          class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 border"
        >
          <div class="flex justify-between items-start mb-2">
            <h4 class="font-semibold text-green-700 dark:text-green-400 text-sm">{{ s.objet }}</h4>
            <span :class="[statusClass(s.statut), 'text-xs px-2 py-1 rounded-full']">
              {{ s.statut_display }}
            </span>
          </div>
          
          <div class="space-y-1 text-sm text-gray-600 dark:text-gray-300 mb-3">
            <p><span class="font-medium">Type:</span> {{ s.type_signalement_display }}</p>
            <p><span class="font-medium">Date:</span> {{ formatDate(s.date_signalement) }}</p>
          </div>
          
          <div class="flex gap-2">
            <button 
              @click="voirDetails(s)"
              class="flex-1 bg-blue-500 text-white px-3 py-2 rounded-lg shadow-md hover:bg-blue-600 hover:shadow-lg transition-all duration-200 text-xs font-medium flex items-center justify-center gap-1"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              Détails
            </button>
            <button 
              @click="modifierSignalement(s)"
              class="flex-1 bg-amber-500 text-white px-3 py-2 rounded-lg shadow-md hover:bg-amber-600 hover:shadow-lg transition-all duration-200 text-xs font-medium flex items-center justify-center gap-1"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              Modifier
            </button>
            <button 
              @click="supprimerSignalement(s.id)"
              class="flex-1 bg-red-500 text-white px-3 py-2 rounded-lg shadow-md hover:bg-red-600 hover:shadow-lg transition-all duration-200 text-xs font-medium flex items-center justify-center gap-1"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              Supprimer
            </button>
          </div>
        </div>
        
        <div v-if="mesSignalements.length === 0" class="text-center py-8 text-gray-500">
          <p class="text-sm">Aucun signalement trouvé.</p>
        </div>
      </div>

      <!-- Version desktop - Table -->
      <div class="hidden sm:block overflow-x-auto">
        <table class="w-full text-left border border-collapse bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
          <thead class="bg-green-100 dark:bg-green-600">
            <tr>
              <th class="p-3 border text-sm font-semibold">Objet</th>
              <th class="p-3 border text-sm font-semibold">Type</th>
              <th class="p-3 border text-sm font-semibold">Date</th>
              <th class="p-3 border text-sm font-semibold">Statut</th>
              <th class="p-3 border text-sm font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in mesSignalements" :key="s.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <td class="p-3 border text-sm">{{ s.objet }}</td>
              <td class="p-3 border text-sm capitalize">{{ s.type_signalement_display }}</td>
              <td class="p-3 border text-sm">{{ formatDate(s.date_signalement) }}</td>
              <td class="p-3 border text-sm">
                <span :class="statusClass(s.statut)">
                  {{ s.statut_display }}
                </span>
              </td>
              <td class="p-3 border text-sm">
                <div class="flex gap-2">
                  <button 
                    @click="voirDetails(s)"
                    class="bg-blue-500 text-white px-3 py-2 rounded-lg shadow-md hover:bg-blue-600 hover:shadow-lg transition-all duration-200 text-xs font-medium flex items-center gap-1"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    Détails
                  </button>
                  <button 
                    @click="modifierSignalement(s)"
                    class="bg-amber-500 text-white px-3 py-2 rounded-lg shadow-md hover:bg-amber-600 hover:shadow-lg transition-all duration-200 text-xs font-medium flex items-center gap-1"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    Modifier
                  </button>
                  <button 
                    @click="supprimerSignalement(s.id)"
                    class="bg-red-500 text-white px-3 py-2 rounded-lg shadow-md hover:bg-red-600 hover:shadow-lg transition-all duration-200 text-xs font-medium flex items-center gap-1"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    Supprimer
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="mesSignalements.length === 0">
              <td colspan="5" class="p-6 text-center text-gray-500">
                Aucun signalement trouvé.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Modal Caméra -->
<!-- Modal Caméra - Template amélioré -->
<div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 w-full max-w-sm sm:max-w-md">
    
    <!-- Titre -->
    <h3 class="text-lg font-semibold text-center mb-4 text-gray-900 dark:text-white">
      Prendre une photo
    </h3>
    
    <!-- Vidéo avec indicateur de chargement -->
    <div class="relative">
<video 
  ref="video" 
  autoplay 
  playsinline 
  muted
  class="w-full h-auto min-h-[200px] rounded-md shadow max-h-60 object-cover"
  :class="{ 'opacity-50': !cameraReady }"
></video>
      
      <!-- Indicateur de chargement -->
      <div v-if="!cameraReady" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-md">
        <div class="text-white text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
          <p class="text-sm">Initialisation de la caméra...</p>
        </div>
      </div>
    </div>

    <!-- Boutons -->
    <div class="mt-4 flex flex-col sm:flex-row gap-3">
      <button 
        @click="capturePhoto" 
        :disabled="!cameraReady"
        :class="[
          'flex-1 px-3 py-2 rounded-md shadow transition-colors text-sm font-medium',
          cameraReady 
            ? 'bg-green-700 text-white hover:bg-green-800' 
            : 'bg-gray-400 text-gray-600 cursor-not-allowed'
        ]"
      >
        Capturer
      </button>
      <button 
        @click="closeCameraModal" 
        class="flex-1 bg-red-600 text-white px-3 py-2 rounded-md shadow hover:bg-red-700 transition-colors text-sm font-medium"
      >
        ❌ Annuler
      </button>
    </div>

    <!-- Debug info (à supprimer en production) -->
    <div v-if="video && showDebugInfo" class="mt-2 text-xs text-gray-500 dark:text-gray-400">
      <p>ReadyState: {{ video.readyState }}/4</p>
      <p>Dimensions: {{ video.videoWidth }}x{{ video.videoHeight }}</p>
      <p>Temps: {{ video.currentTime?.toFixed(2) }}s</p>
    </div>

    <!-- Canvas caché -->
    <canvas ref="canvas" class="hidden"></canvas>
  </div>
</div>


  <!-- Modal Détails -->
  <div v-if="showDetails && selectedSignalement" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
      <!-- Header -->
      <div class="flex justify-between items-center p-4 sm:p-6 border-b">
        <h3 class="text-lg sm:text-xl font-semibold text-green-700 dark:text-green-400">
          Détails du signalement
        </h3>
        <button 
          @click="showDetails = false" 
          class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-xl sm:text-2xl"
        >
          ✕
        </button>
      </div>
      
      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-4 sm:p-6">
        <div class="space-y-4">
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <span class="font-semibold text-green-700 dark:text-green-400">Objet:</span>
            <p class="mt-1 text-sm sm:text-base">{{ selectedSignalement.objet }}</p>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
              <span class="font-semibold text-green-700 dark:text-green-400">Type:</span>
              <p class="mt-1 text-sm sm:text-base">{{ selectedSignalement.type_signalement_display }}</p>
            </div>
            
            <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
              <span class="font-semibold text-green-700 dark:text-green-400">Statut:</span>
              <p class="mt-1">
                <span :class="statusClass(selectedSignalement.statut)" class="text-sm sm:text-base">
                  {{ selectedSignalement.statut_display }}
                </span>
              </p>
            </div>
          </div>
          
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <span class="font-semibold text-green-700 dark:text-green-400">Description:</span>
            <p class="mt-1 text-sm sm:text-base">{{ selectedSignalement.description }}</p>
          </div>
          
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <span class="font-semibold text-green-700 dark:text-green-400">Localisation:</span>
            <p class="mt-1 text-sm sm:text-base">{{ selectedSignalement.localisation }}</p>
          </div>
          <!-- À ajouter dans la modal détails, après la section "Localisation" et avant les dates -->
<div v-if="selectedSignalement.photo_url" class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
  <span class="font-semibold text-green-700 dark:text-green-400 block mb-2">Photo:</span>
  <div class="flex justify-center">
    <img 
      :src="selectedSignalement.photo_url" 
      :alt="`Photo du signalement: ${selectedSignalement.objet}`"
      class="max-w-full max-h-64 object-contain rounded-lg shadow-md cursor-pointer hover:shadow-lg transition-shadow"
      @click="ouvrirPhotoEnGrandFormat"
    />
  </div>
  <p class="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
    Cliquez sur l'image pour l'agrandir
  </p>
</div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
              <span class="font-semibold text-green-700 dark:text-green-400">Date de signalement:</span>
              <p class="mt-1 text-sm sm:text-base">{{ formatDate(selectedSignalement.date_signalement) }}</p>
            </div>
            
            <div v-if="selectedSignalement.date_resolution" class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
              <span class="font-semibold text-green-700 dark:text-green-400">Date de résolution:</span>
              <p class="mt-1 text-sm sm:text-base">{{ formatDate(selectedSignalement.date_resolution) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

// Remplacer l'interface Signalement existante par celle-ci :
interface Signalement {
  id: number
  objet: string
  description: string
  type_signalement: string
  type_signalement_display: string
  date_signalement: string
  date_resolution?: string
  statut: string
  statut_display: string
  localisation: string
  utilisateur_nom: string
  photo_id?: number
  photo_url?: string 
}

interface Choice {
  value: string
  label: string
}

// État global
const loading = ref(false)
const token = localStorage.getItem('authToken')

// Formulaire
const selectedType = ref('pollution')
const objet = ref('')
const localisation = ref('')
const description = ref('')
const file = ref<File | null>(null)

// Aperçu de la photo
const photoPreview = ref<string | null>(null)

// Géolocalisation
const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)
const useAutoLocation = ref(false)
const locationStatus = ref<'loading' | 'success' | 'error' | null>(null)
const locationError = ref('')

// Données
const mesSignalements = ref<Signalement[]>([])
const typeChoices = ref<Choice[]>([
  { value: 'pollution', label: 'Pollution' },
  { value: 'dechets', label: 'Déchets' },
  { value: 'climat', label: 'Climat' }
])

const statutChoices = ref<Choice[]>([
  { value: 'en_attente', label: 'En attente' },
  { value: 'en_cours', label: 'En cours' },
  { value: 'traite', label: 'Traité' }
])

// Caméra
const showCamera = ref(false)
const video = ref<HTMLVideoElement | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)
let stream: MediaStream | null = null

// Modal détails
const showDetails = ref(false)
const selectedSignalement = ref<Signalement | null>(null)

// Fonction pour créer l'aperçu de la photo
const createPhotoPreview = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    photoPreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

// Fonction pour supprimer la photo
const removePhoto = () => {
  file.value = null
  photoPreview.value = null
}

// Fonction pour formater la taille du fichier
const formatFileSize = (bytes?: number): string => {
  if (!bytes) return ''
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

// Gestion de la géolocalisation
const getCurrentLocation = async (): Promise<{ latitude: number; longitude: number }> => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Géolocalisation non supportée par ce navigateur'))
      return
    }

    locationStatus.value = 'loading'
    
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const coords = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }
        locationStatus.value = 'success'
        resolve(coords)
      },
      (error) => {
        locationStatus.value = 'error'
        let errorMessage = 'Erreur de géolocalisation'
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Permission de géolocalisation refusée'
            break
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Position non disponible'
            break
          case error.TIMEOUT:
            errorMessage = 'Timeout de géolocalisation'
            break
        }
        
        locationError.value = errorMessage
        reject(new Error(errorMessage))
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000
      }
    )
  })
}

// Toggle géolocalisation automatique
const toggleAutoLocation = async () => {
  if (useAutoLocation.value) {
    try {
      const coords = await getCurrentLocation()
      latitude.value = coords.latitude
      longitude.value = coords.longitude
    } catch (error) {
      console.error('Erreur de géolocalisation:', error)
      useAutoLocation.value = false
    }
  } else {
    locationStatus.value = null
    locationError.value = ''
  }
}

// Gestion des fichiers - CORRIGÉ pour correspondre au template
const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    file.value = target.files[0]
    createPhotoPreview(target.files[0])
  }
}

// Gestion de la caméra
const openCameraModal = async () => {
  // Récupérer la géolocalisation si l'option auto est activée
  if (useAutoLocation.value && (!latitude.value || !longitude.value)) {
    try {
      await toggleAutoLocation()
    } catch (error) {
      console.error('Erreur lors de la récupération de la position:', error)
    }
  }
  
  startCamera()
}

const cameraReady = ref(false)
const showDebugInfo = ref(false)

const startCamera = async (): Promise<void> => {
  showCamera.value = true
  cameraReady.value = false
  await nextTick()

  if (navigator.mediaDevices?.getUserMedia) {
    try {
      // Essayer d'abord avec la caméra arrière, puis avant si échec
      let constraints = { 
        video: { 
          facingMode: 'environment',
          width: { ideal: 640 },
          height: { ideal: 480 }
        }, 
        audio: false 
      }

      try {
        stream = await navigator.mediaDevices.getUserMedia(constraints)
      } catch (backCameraError) {
        console.log('Caméra arrière non disponible, essai avec caméra avant')
        constraints = { 
          video: { 
            facingMode: 'user',
            width: { ideal: 1280},
            height: { ideal: 720}
          }, 
          audio: false 
        }
        stream = await navigator.mediaDevices.getUserMedia(constraints)
      }

      if (video.value && stream) {
        video.value.srcObject = stream
        
        // Version simplifiée de l'initialisation vidéo
        video.value.onloadedmetadata = (): void => {
          console.log('Métadonnées chargées')
          if (video.value) {
            video.value.play().then(() => {
              // Attendre un peu que la vidéo se stabilise
              setTimeout(() => {
                cameraReady.value = true
              }, 1000)
            }).catch(console.error)
          }
        }
      }
    } catch (error) {
      console.error('Erreur caméra:', error)
      let errorMessage = 'Impossible d\'accéder à la caméra.'
      
      if (typeof error === 'object' && error !== null && 'name' in error) {
        const err = error as { name: string }
        if (err.name === 'NotAllowedError') {
          errorMessage = 'Permission caméra refusée. Veuillez autoriser l\'accès à la caméra dans les paramètres de votre navigateur.'
        } else if (err.name === 'NotFoundError') {
          errorMessage = 'Aucune caméra trouvée sur cet appareil.'
        } else if (err.name === 'NotReadableError') {
          errorMessage = 'La caméra est déjà utilisée par une autre application.'
        }
      }
      
      alert(errorMessage)
      showCamera.value = false
      cameraReady.value = false
    }
  } else {
    alert('Votre navigateur ne supporte pas l\'accès à la caméra.')
    showCamera.value = false
    cameraReady.value = false
  }
}

const capturePhoto = (): void => {
  if (!video.value || !canvas.value || !cameraReady.value) {
    alert('La caméra n\'est pas encore prête')
    return
  }
  
  // Forcer une actualisation de la vidéo avant capture
  if (video.value) {
    video.value.play()
  }
  
  // Attendre un petit délai puis capturer
  setTimeout(() => {
    // Vérifier que la vidéo a des dimensions valides
    if (!video.value || video.value.videoWidth === 0 || video.value.videoHeight === 0) {
      console.error('Vidéo non prête - dimensions nulles')
      alert('La caméra n\'est pas encore prête. Attendez quelques secondes et réessayez.')
      return
    }
    
    console.log('Capture en cours - Dimensions vidéo:', video.value.videoWidth, 'x', video.value.videoHeight)
    const context = canvas.value?.getContext('2d')
    
    if (context && canvas.value) {
      // Définir les dimensions du canvas selon celles de la vidéo
      canvas.value.width = video.value.videoWidth
      canvas.value.height = video.value.videoHeight
     
      // Vérifier que le contexte est valide
      if (canvas.value.width > 0 && canvas.value.height > 0) {
        // Dessiner l'image vidéo sur le canvas
        context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
       
        // Vérification simplifiée de l'image (optionnelle et moins stricte)
        try {
          const imageData = context.getImageData(0, 0, Math.min(100, canvas.value.width), Math.min(100, canvas.value.height))
          const data = imageData.data
          let totalBrightness = 0
          let pixelCount = 0
         
          // Calculer la luminosité moyenne sur un échantillon
          for (let i = 0; i < data.length; i += 4) {
            const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3
            totalBrightness += brightness
            pixelCount++
          }
         
          const averageBrightness = totalBrightness / pixelCount
          console.log('Luminosité moyenne de l\'image:', averageBrightness)
         
          // Seuil plus bas et avertissement au lieu d'échec
          if (averageBrightness < 5) {
            console.warn('Image semble très sombre, mais on continue')
            // On peut afficher un avertissement mais on continue quand même
            if (!confirm('L\'image semble très sombre. Voulez-vous quand même l\'utiliser ?')) {
              return
            }
          }
        } catch (imageCheckError) {
          console.warn('Impossible de vérifier l\'image, on continue quand même:', imageCheckError)
          // On continue même si la vérification échoue
        }
       
        // Convertir en blob avec une qualité élevée
        canvas.value.toBlob((blob: Blob | null) => {
          if (blob) {
            // Créer un objet File à partir du blob
            const capturedFile = new File([blob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' })
            file.value = capturedFile
            createPhotoPreview(capturedFile)
            console.log('Photo capturée avec succès:', capturedFile.size, 'bytes')
            closeCameraModal()
          } else {
            console.error('Impossible de créer le blob')
            alert('Erreur lors de la capture de l\'image')
          }
        }, 'image/jpeg', 0.9) // Qualité élevée
      } else {
        console.error('Dimensions du canvas invalides')
        alert('Erreur: dimensions de l\'image invalides')
      }
    } else {
      console.error('Impossible d\'obtenir le contexte du canvas')
      alert('Erreur technique lors de la capture')
    }
  }, 200)
}

const closeCameraModal = () => {
  showCamera.value = false
  cameraReady.value = false
  
  if (stream) {
    stream.getTracks().forEach(track => {
      track.stop()
      console.log('Track arrêté:', track.kind)
    })
    stream = null
  }
  
  // Nettoyer la source vidéo
  if (video.value) {
    video.value.srcObject = null
    video.value.onloadedmetadata = null
    video.value.oncanplay = null
    video.value.onerror = null
  }
}

// Fonction utilitaire pour vérifier l'état de la caméra
// const checkCameraStatus = () => {
//   if (video.value) {
//     console.log('État vidéo:', {
//       readyState: video.value.readyState,
//       videoWidth: video.value.videoWidth,
//       videoHeight: video.value.videoHeight,
//       currentTime: video.value.currentTime,
//       paused: video.value.paused
//     })
//   }
// }

// Formatage des dates
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Classes CSS pour les statuts
const statusClass = (statut: string): string => {
  switch (statut) {
    case 'en_attente':
      return 'bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium'
    case 'en_cours':
      return 'bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium'
    case 'traite':
      return 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium'
    default:
      return 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-medium'
  }
}

// Envoi du signalement - CORRIGÉ pour correspondre au template
const submitSignalement = async () => {
  if (!objet.value || !description.value || !selectedType.value || !localisation.value) {
    alert('Veuillez remplir tous les champs obligatoires')
    return
  }

  // Vérifier si les coordonnées sont présentes
  if (!latitude.value || !longitude.value) {
    alert('Veuillez renseigner la localisation (latitude et longitude)')
    return
  }

  loading.value = true

  try {
    const formData = new FormData()
    formData.append('objet', objet.value)
    formData.append('description', description.value)
    formData.append('type_signalement', selectedType.value)
    formData.append('localisation', localisation.value)
    formData.append('latitude', latitude.value.toString())
    formData.append('longitude', longitude.value.toString())
    
    if (file.value) {
      formData.append('photo', file.value)
    }

    const response = await fetch('http://localhost:8000/api/signalements/create/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })

    if (response.ok) {
      alert('Signalement envoyé avec succès!')
      // Réinitialiser le formulaire
      resetForm()
      // Recharger la liste des signalements
      await chargerMesSignalements()
    } else {
      const errorData = await response.json()
      alert(`Erreur lors de l'envoi: ${errorData.message || 'Erreur inconnue'}`)
    }
  } catch (error) {
    console.error('Erreur lors de l\'envoi:', error)
    alert('Erreur lors de l\'envoi du signalement')
  } finally {
    loading.value = false
  }
}

// Réinitialiser le formulaire
const resetForm = () => {
  objet.value = ''
  description.value = ''
  localisation.value = ''
  selectedType.value = 'pollution'
  file.value = null
  photoPreview.value = null
  latitude.value = null
  longitude.value = null
  useAutoLocation.value = false
  locationStatus.value = null
  locationError.value = ''
}

// Charger mes signalements (pour citoyen)
const chargerMesSignalements = async () => {
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch('http://localhost:8000/api/signalements/mes-signalements/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      mesSignalements.value = data.signalements || []
    }
  } catch (error) {
    console.error('Erreur lors du chargement des signalements:', error)
  }
}

// Charger les choix disponibles
import { apiClient } from '@/services/apiClient';

const chargerChoix = async () => {
  try {
    const client = apiClient();
    const response = await client('http://localhost:8000/api/signalements/choices/');
    if (response.ok) {
      const data = await response.json();
      if (data.types_signalement) {
        typeChoices.value = data.types_signalement;
      }
      if (data.statuts) {
        statutChoices.value = data.statuts;
      }
    }
  } catch (error) {
    console.error('Erreur lors du chargement des choix:', error);
  }
};

// Afficher les détails d'un signalement - CORRIGÉ pour correspondre au template
const voirDetails = (signalement: Signalement) => {
  selectedSignalement.value = signalement
  showDetails.value = true
}

const ouvrirPhotoEnGrandFormat = () => {
  if (selectedSignalement.value?.photo_url) {
    window.open(selectedSignalement.value.photo_url, '_blank')
  }
}
// Modifier un signalement - AJOUTÉ pour correspondre au template
const modifierSignalement = (signalement: Signalement) => {
  // Pré-remplir le formulaire avec les données du signalement
  objet.value = signalement.objet
  description.value = signalement.description
  localisation.value = signalement.localisation
  selectedType.value = signalement.type_signalement
  
  // Scroll vers le formulaire
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Supprimer un signalement - AJOUTÉ pour correspondre au template
const supprimerSignalement = async (id: number) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce signalement ?')) {
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/signalements/delete/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      alert('Signalement supprimé avec succès!')
      await chargerMesSignalements()
    } else {
      alert('Erreur lors de la suppression du signalement')
    }
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    alert('Erreur lors de la suppression du signalement')
  }
}

// Initialisation
onMounted(() => {
  chargerMesSignalements()
})
</script>

<style scoped>
/* Styles pour très petits écrans (320px et moins) */
@media (max-width: 320px) {
  .text-xl {
    font-size: 1.125rem;
  }
  
  .px-4 {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }
}

/* Styles pour mobiles (321px à 640px) */
@media (min-width: 321px) and (max-width: 640px) {
  .container-mobile {
    padding: 0 1rem;
  }
  
  .grid-mobile {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

/* Styles pour tablettes (641px à 1024px) */
@media (min-width: 641px) and (max-width: 1024px) {
  .container-tablet {
    max-width: 100%;
    padding: 0 2rem;
  }
  
  .grid-tablet {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* Styles pour desktop (1025px et plus) */
@media (min-width: 1025px) {
  .container-desktop {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .grid-desktop {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
}

/* Animations et transitions */
.transition-colors {
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Amélioration de l'accessibilité */
.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.5);
}

/* Scrollbar personnalisée pour webkit */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #16a34a;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #15803d;
}

/* Amélioration du style des input files */
input[type="file"]::-webkit-file-upload-button {
  background: #dcfce7;
  color: #166534;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

input[type="file"]::-webkit-file-upload-button:hover {
  background: #bbf7d0;
}
</style>
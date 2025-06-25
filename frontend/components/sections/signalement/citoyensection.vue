<!-- section citoyensection -->
<template>
  <div class="bg-white rounded-lg shadow p-4 sm:p-6 mb-6 sm:mb-8 dark:bg-gray-600 mx-2 sm:mx-0">
    <h2 class="text-xl sm:text-2xl lg:text-3xl text-center font-semibold text-green-700 mb-4 sm:mb-6 dark:text-green-600">
      Faire un signalement
    </h2>

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

    <div class="space-y-4 mb-4 sm:mb-6">
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

      <textarea 
        v-model="description" 
        placeholder="Description détaillée du problème" 
        class="border rounded-lg p-3 w-full h-24 sm:h-28 text-sm sm:text-base resize-none focus:ring-2 focus:ring-green-500 focus:border-transparent" 
        required
      ></textarea>
        </div>
      
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

        <div v-if="file || photoPreview" class="bg-green-50 dark:bg-green-900 p-4 rounded-lg border border-green-200 dark:border-green-700">
          <div class="flex items-start gap-4">
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

  <div class="bg-white rounded-lg shadow mx-2 sm:mx-0 dark:bg-gray-600">
    <div class="bg-green-600 text-white p-4 sm:p-6 font-semibold rounded-t-lg">
      <h3 class="text-lg sm:text-xl">Mes signalements ({{ mesSignalements.length }})</h3>
    </div>
    
    <div class="p-4 sm:p-6 bg-gray-50 dark:bg-gray-600">
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

  <div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 w-full max-w-sm sm:max-w-md">
    
    <h3 class="text-lg font-semibold text-center mb-4 text-gray-900 dark:text-white">
      Prendre une photo
    </h3>
    
    <div class="relative">
      <video 
        ref="video" 
        autoplay 
        playsinline 
        muted
        class="w-full h-auto min-h-[200px] rounded-md shadow max-h-60 object-cover"
        :class="{ 'opacity-50': !cameraReady }"
      ></video>
      
      <div v-if="!cameraReady && !cameraError" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-md">
        <div class="text-white text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
          <p class="text-sm">Initialisation de la caméra...</p>
        </div>
      </div>

      <div v-if="cameraError" class="absolute inset-0 flex items-center justify-center bg-red-800 bg-opacity-80 rounded-md text-white p-4 text-center">
        <p class="text-base font-semibold">{{ cameraError }}</p>
      </div>
    </div>

    <div class="mt-4 flex flex-col sm:flex-row gap-3">
      <button 
        @click="capturePhoto" 
        :disabled="!cameraReady || !!cameraError"
        :class="[
          'flex-1 px-3 py-2 rounded-md shadow transition-colors text-sm font-medium',
          !cameraReady || !!cameraError
            ? 'bg-gray-400 text-gray-600 cursor-not-allowed'
            : 'bg-green-700 text-white hover:bg-green-800' 
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

    <div v-if="video && showDebugInfo" class="mt-2 text-xs text-gray-500 dark:text-gray-400">
      <p>ReadyState: {{ video.readyState }}/4</p>
      <p>Dimensions: {{ video.videoWidth }}x{{ video.videoHeight }}</p>
      <p>Temps: {{ video.currentTime?.toFixed(2) }}s</p>
    </div>

    <canvas ref="canvas" class="hidden"></canvas>
  </div>
</div>


  <div v-if="showDetails && selectedSignalement" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
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
const cameraReady = ref(false)
const cameraError = ref<string | null>(null) // New ref for camera errors
const showDebugInfo = ref(false) // Keep this for debugging if needed

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

// Gestion des fichiers
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

const startCamera = async (): Promise<void> => {
  showCamera.value = true
  cameraReady.value = false
  cameraError.value = null // Reset camera error on open
  await nextTick() // Ensure video element is in DOM

  if (navigator.mediaDevices?.getUserMedia) {
    try {
      let constraints: MediaStreamConstraints = { 
        video: { 
          facingMode: 'environment', // Try back camera first
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }, 
        audio: false 
      }

      try {
        stream = await navigator.mediaDevices.getUserMedia(constraints)
      } catch (backCameraError: any) {
        console.warn('Back camera not available, trying front camera:', backCameraError)
        // If back camera fails, try front camera
        constraints = { 
          video: { 
            facingMode: 'user', 
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }, 
          audio: false 
        }
        stream = await navigator.mediaDevices.getUserMedia(constraints)
      }

      if (video.value && stream) {
        video.value.srcObject = stream
        
        video.value.onloadedmetadata = (): void => {
          console.log('Video metadata loaded.')
          video.value?.play().then(() => {
            console.log('Video playback started.')
            // Wait for a brief moment for the stream to stabilize and render frames
            setTimeout(() => {
              cameraReady.value = true
              console.log('Camera ready: true')
            }, 500); // Increased timeout for better stability
          }).catch(playError => {
            console.error('Error playing video stream:', playError)
            cameraError.value = 'Impossible de lire le flux vidéo de la caméra. (' + playError.name + ')'
            stopCamera()
          })
        }
      } else {
        cameraError.value = "Impossible d'initialiser le lecteur vidéo."
        stopCamera()
      }
    } catch (error: any) {
      console.error('Camera access error:', error)
      let errorMessage = 'Impossible d\'accéder à la caméra.'
      
      if (error.name === 'NotAllowedError') {
        errorMessage = 'Permission caméra refusée. Veuillez autoriser l\'accès à la caméra dans les paramètres de votre navigateur.'
      } else if (error.name === 'NotFoundError') {
        errorMessage = 'Aucune caméra trouvée sur cet appareil.'
      } else if (error.name === 'NotReadableError') {
        errorMessage = 'La caméra est déjà utilisée par une autre application ou est déconnectée.'
      } else if (error.name === 'OverconstrainedError') {
        errorMessage = 'La caméra ne peut pas satisfaire les contraintes demandées (résolution, mode). Essayez avec une résolution différente.'
      } else if (error.name === 'AbortError') {
        errorMessage = 'L\'opération de la caméra a été interrompue.'
      }
      
      cameraError.value = errorMessage
      stopCamera()
    }
  } else {
    cameraError.value = 'Votre navigateur ne supporte pas l\'accès à la caméra (getUserMedia non disponible).'
    stopCamera()
  }
}

const capturePhoto = (): void => {
  if (!video.value || !canvas.value || !cameraReady.value) {
    // This alert should ideally not be reached if buttons are disabled correctly
    alert('La caméra n\'est pas encore prête ou une erreur est survenue.')
    return
  }
  
  // Ensure the video is playing just before capture
  if (video.value.paused) {
    video.value.play().catch(e => console.error("Error ensuring video playback:", e));
  }

  // Add a small delay to allow for fresh frame rendering, crucial for some devices
  setTimeout(() => {
    if (!video.value || video.value.videoWidth === 0 || video.value.videoHeight === 0) {
      console.error('Video element has no dimensions, cannot capture.')
      alert('La caméra n\'a pas pu fournir une image valide. Veuillez réessayer.')
      return
    }
    
    console.log('Attempting capture - Video Dimensions:', video.value.videoWidth, 'x', video.value.videoHeight)
    const context = canvas.value?.getContext('2d')
    
    if (context && canvas.value) {
      canvas.value.width = video.value.videoWidth
      canvas.value.height = video.value.videoHeight
     
      try {
        context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
        const imageData = context.getImageData(0, 0, canvas.value.width, canvas.value.height)
        const data = imageData.data
        let totalBrightness = 0
        
        // Sample a portion of the image for brightness check to be faster
        const step = 4 * 10; // Check every 10th pixel
        for (let i = 0; i < data.length; i += step) {
          const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3
          totalBrightness += brightness
        }
        const pixelCount = data.length / step;
        const averageBrightness = totalBrightness / pixelCount
        
        console.log('Average image brightness:', averageBrightness)
        
        // Threshold for very dark images
        if (averageBrightness < 10) { // Slightly increased threshold for warning
          console.warn('Image seems very dark.')
          if (!confirm('L\'image semble très sombre. Elle pourrait être illisible. Voulez-vous quand même l\'utiliser ?')) {
            return
          }
        }

        canvas.value.toBlob((blob) => {
          if (blob) {
            const capturedFile = new File([blob], `photo_${Date.now()}.png`, { type: 'image/png' })
            file.value = capturedFile
            createPhotoPreview(capturedFile)
            closeCameraModal()
          } else {
            alert('Erreur lors de la création du fichier image.')
          }
        }, 'image/png')

      } catch (drawError) {
        console.error('Error drawing image to canvas:', drawError)
        alert('Impossible de capturer la photo. Le flux vidéo n\'est peut-être pas valide.')
      }
    } else {
      alert('Le canvas n\'est pas disponible pour la capture.')
    }
  }, 100); // Small delay to ensure frame is drawn
}

const closeCameraModal = () => {
  stopCamera()
  showCamera.value = false
  cameraError.value = null // Clear any camera errors when closing
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
  if (video.value) {
    video.value.srcObject = null // Clear the source object
  }
  cameraReady.value = false
}

// Fetch signalements from API (placeholder)
const fetchSignalements = async () => {
  // Mock data for demonstration
  mesSignalements.value = [
    { id: 1, objet: 'Déversement sauvage', description: 'Beaucoup de sacs poubelles jetés en bord de route.', type_signalement: 'dechets', type_signalement_display: 'Déchets', date_signalement: '2023-10-26T10:00:00Z', statut: 'en_attente', statut_display: 'En attente', localisation: 'Rue Principale 123', utilisateur_nom: 'Citoyen Lambda', photo_url: 'https://via.placeholder.com/150/FF0000/FFFFFF?text=Dechets1' },
    { id: 2, objet: 'Fumée anormale', description: 'Une usine émet une fumée épaisse et noire.', type_signalement: 'pollution', type_signalement_display: 'Pollution', date_signalement: '2023-10-25T14:30:00Z', date_resolution: '2023-10-26T09:00:00Z', statut: 'traite', statut_display: 'Traité', localisation: 'Zone Industrielle Z', utilisateur_nom: 'Citoyen Lambda', photo_url: 'https://via.placeholder.com/150/0000FF/FFFFFF?text=Pollution1' },
    { id: 3, objet: 'Arbre tombé', description: 'Un grand arbre est tombé et bloque la route.', type_signalement: 'climat', type_signalement_display: 'Climat', date_signalement: '2023-10-24T08:15:00Z', statut: 'en_cours', statut_display: 'En cours', localisation: 'Avenue des Fleurs', utilisateur_nom: 'Citoyen Lambda', photo_url: 'https://via.placeholder.com/150/008000/FFFFFF?text=Climat1' }
  ].sort((a, b) => new Date(b.date_signalement).getTime() - new Date(a.date_signalement).getTime());
}

// Submit signalement (placeholder)
const submitSignalement = async () => {
  loading.value = true;
  try {
    // Here you would typically send data to your backend API
    console.log({
      type: selectedType.value,
      objet: objet.value,
      localisation: localisation.value,
      latitude: latitude.value,
      longitude: longitude.value,
      description: description.value,
      file: file.value, // This would be part of FormData for actual upload
      token: token
    });

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000)); 

    alert('Signalement envoyé avec succès !');

    // Reset form
    objet.value = '';
    localisation.value = '';
    description.value = '';
    file.value = null;
    photoPreview.value = null;
    latitude.value = null;
    longitude.value = null;
    useAutoLocation.value = false;
    locationStatus.value = null;

    // Refresh the list of signalements (mock refresh)
    fetchSignalements();

  } catch (error) {
    console.error('Erreur lors de l\'envoi du signalement:', error);
    alert('Échec de l\'envoi du signalement.');
  } finally {
    loading.value = false;
  }
};

// --- Utility functions for table/cards ---
const formatDate = (dateString: string): string => {
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('fr-FR', options);
};

const statusClass = (status: string): string => {
  switch (status) {
    case 'en_attente':
      return 'bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium dark:bg-yellow-800 dark:text-yellow-100';
    case 'en_cours':
      return 'bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium dark:bg-blue-800 dark:text-blue-100';
    case 'traite':
      return 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium dark:bg-green-800 dark:text-green-100';
    default:
      return 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-medium dark:bg-gray-700 dark:text-gray-300';
  }
};

const voirDetails = (signalement: Signalement) => {
  selectedSignalement.value = signalement;
  showDetails.value = true;
};

const modifierSignalement = (signalement: Signalement) => {
  alert(`Fonctionnalité de modification pour le signalement "${signalement.objet}" à implémenter.`);
  // Here you would populate the form with signalement data for editing
};

const supprimerSignalement = async (id: number) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce signalement ?')) {
    // Simulate API call for deletion
    console.log(`Suppression du signalement avec l'ID: ${id}`);
    await new Promise(resolve => setTimeout(resolve, 500));
    mesSignalements.value = mesSignalements.value.filter(s => s.id !== id);
    alert('Signalement supprimé avec succès !');
  }
};

// This function is new for opening the photo in a larger format (e.g., new tab)
const ouvrirPhotoEnGrandFormat = () => {
  if (selectedSignalement.value?.photo_url) {
    window.open(selectedSignalement.value.photo_url, '_blank');
  }
};


// Lifecycle hook
onMounted(() => {
  fetchSignalements();
  if (useAutoLocation.value) {
    toggleAutoLocation(); // Attempt to get location on mount if auto is enabled
  }
});
</script>

<style scoped>
/* You can add or modify styles here if needed */
</style>

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
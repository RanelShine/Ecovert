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

      <!-- Description -->
      <textarea 
        v-model="description" 
        placeholder="Description détaillée du problème" 
        class="border rounded-lg p-3 w-full h-24 sm:h-28 text-sm sm:text-base resize-none focus:ring-2 focus:ring-green-500 focus:border-transparent" 
        required
      ></textarea>

      <!-- Upload de fichier et caméra -->
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
          📷 Prendre une photo
        </button>
      </div>

      <!-- Indicateur de fichier sélectionné -->
      <div v-if="file" class="text-sm text-green-600 bg-green-50 p-3 rounded-lg">
        ✓ Photo sélectionnée : {{ file.name }}
      </div>
    </div>

    <!-- Bouton de soumission -->
    <button
      @click="submitSignalement"
      :disabled="loading || !objet || !localisation || !description || !file"
      :class="[
        'w-full px-6 py-3 sm:py-4 rounded-lg shadow text-sm sm:text-base font-semibold transition-colors',
        loading || !objet || !localisation || !description || !file
          ? 'bg-gray-400 cursor-not-allowed text-gray-600'
          : 'bg-green-700 hover:bg-green-800 text-white'
      ]"
    >
      {{ loading ? 'Envoi en cours...' : 'Envoyer le signalement' }}
    </button>
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
  <div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-75 flex flex-col items-center justify-center z-50 p-4">
    <div class="w-full max-w-md sm:max-w-lg lg:max-w-xl">
      <video 
        ref="video" 
        autoplay 
        playsinline 
        class="w-full rounded-lg shadow-lg max-h-[50vh] sm:max-h-[60vh] object-cover"
      ></video>
    </div>
    
    <div class="mt-4 sm:mt-6 flex flex-col sm:flex-row gap-3 sm:gap-4 w-full max-w-md sm:max-w-none">
      <button 
        @click="capturePhoto" 
        class="flex-1 bg-green-700 text-white px-4 py-3 rounded-lg shadow hover:bg-green-800 transition-colors text-sm sm:text-base"
      >
        📸 Prendre la photo
      </button>
      <button 
        @click="closeCameraModal" 
        class="flex-1 bg-red-600 text-white px-4 py-3 rounded-lg shadow hover:bg-red-700 transition-colors text-sm sm:text-base"
      >
        ❌ Annuler
      </button>
    </div>
    <canvas ref="canvas" class="hidden"></canvas>
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
const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

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

// Gestion de la caméra
const openCameraModal = async () => {
  if (!navigator.geolocation) {
    alert('Géolocalisation non supportée.')
    return
  }

  navigator.geolocation.getCurrentPosition(
    position => {
      latitude.value = position.coords.latitude
      longitude.value = position.coords.longitude
      startCamera()
    },
    error => {
      alert('Erreur de géolocalisation.')
    }
  )
}

const startCamera = async () => {
  showCamera.value = true
  await nextTick()

  if (navigator.mediaDevices?.getUserMedia) {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' }, 
        audio: false 
      })
      if (video.value) {
        video.value.srcObject = stream
        await video.value.play()
      }
    } catch {
      alert('Impossible d\'accéder à la caméra.')
      showCamera.value = false
    }
  }
}

const closeCameraModal = () => {
  showCamera.value = false
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
}

const capturePhoto = () => {
  if (!video.value || !canvas.value) return

  const width = video.value.videoWidth
  const height = video.value.videoHeight
  canvas.value.width = width
  canvas.value.height = height

  const ctx = canvas.value.getContext('2d')
  if (!ctx) return

  ctx.drawImage(video.value, 0, 0, width, height)
  canvas.value.toBlob(blob => {
    if (blob) {
      file.value = new File([blob], 'photo.jpg', { type: 'image/jpeg' })
      alert('Photo prise avec succès !')
      closeCameraModal()
    }
  }, 'image/jpeg', 0.95)
}

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    file.value = target.files[0]
  }
}

// Soumettre un signalement
const submitSignalement = async () => {
  if (!file.value) {
    alert('Veuillez prendre ou importer une photo.')
    return
  }

  loading.value = true

  try {
    
    // Upload de la photo
    const photoFormData = new FormData()
    photoFormData.append('image', file.value)
    if (latitude.value !== null) photoFormData.append('latitude', latitude.value.toString())
    if (longitude.value !== null) photoFormData.append('longitude', longitude.value.toString())

    const photoResponse = await fetch('http://localhost:8000/api/photos/upload-photo/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: photoFormData
    })

    if (!photoResponse.ok) throw new Error('Erreur lors de l\'upload de la photo')

    const photoData = await photoResponse.json()

    // Création du signalement
    const signalementPayload = {
      objet: objet.value,
      localisation: localisation.value,
      description: description.value,
      type_signalement: selectedType.value,
      photo_id: photoData.id
    }

    const response = await fetch('http://localhost:8000/api/signalements/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(signalementPayload)
    })

    if (!response.ok) throw new Error('Erreur lors de la création du signalement')

    alert('Signalement envoyé avec succès !')
    
    // Réinitialiser le formulaire
    objet.value = ''
    localisation.value = ''
    description.value = ''
    file.value = null
    selectedType.value = 'pollution'
    
    // Recharger la liste
    await chargerMesSignalements()
    
  } catch (error) {
    alert('Erreur: ' + error)
  } finally {
    loading.value = false
  }
}

// Supprimer un signalement
const supprimerSignalement = async (signalementId: number) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce signalement ?')) {
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/signalements/delete/${signalementId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      alert('Signalement supprimé avec succès !')
      await chargerMesSignalements()
    } else {
      throw new Error('Erreur lors de la suppression')
    }
  } catch (error) {
    alert('Erreur: ' + error)
  }
}

// Modifier un signalement
const modifierSignalement = async (signalement: Signalement) => {
  // Préremplir le formulaire avec les données du signalement
  selectedType.value = signalement.type_signalement
  objet.value = signalement.objet
  localisation.value = signalement.localisation
  description.value = signalement.description
  
  // Faire défiler vers le formulaire
  window.scrollTo({ top: 0, behavior: 'smooth' })
  
  // Optionnel: vous pouvez ajouter une logique pour gérer l'édition
  // Par exemple, stocker l'ID du signalement en cours de modification
  // signalementEnEdition.value = signalement.id
}
const voirDetails = async (signalement: Signalement) => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    console.error('Aucun token trouvé.')
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/signalements/detail/${signalement.id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Erreur lors de la récupération du détail:', errorData);
      return;
    }

    const data = await response.json();
    selectedSignalement.value = data;
    showDetails.value = true;
  } catch (error) {
    console.error('Erreur réseau:', error);
  }
};

// Utilitaires
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
    case 'en_cours': return 'text-yellow-600 font-semibold bg-yellow-100 px-2 py-1 rounded-full'
    case 'traite': return 'text-green-600 font-semibold bg-green-100 px-2 py-1 rounded-full'
    case 'en_attente': return 'text-gray-600 font-semibold bg-gray-100 px-2 py-1 rounded-full'
    default: return 'text-gray-600 bg-gray-100 px-2 py-1 rounded-full'
  }
}

// Initialisation
onMounted(async () => {
  await chargerChoix()
  await chargerMesSignalements()
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
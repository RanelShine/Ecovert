<!-- section citoyensection -->
<template>
  <!-- Formulaire de création -->
  <div class="bg-white rounded-lg shadow p-6 mb-8">
    <h2 class="text-2xl font-semibold text-green-700 mb-4">Faire un signalement</h2>

    <div class="flex gap-2 mb-4">
      <button
        v-for="type in typeChoices"
        :key="type.value"
        @click="selectedType = type.value"
        :class="[
          'px-4 py-2 rounded shadow capitalize',
          selectedType === type.value
            ? 'bg-green-700 text-white'
            : 'bg-green-100 text-green-800'
        ]"
      >
        {{ type.label }}
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <input 
        v-model="objet" 
        type="text" 
        placeholder="Objet du signalement" 
        class="border rounded p-2 w-full" 
        required
      />
      <input 
        v-model="localisation" 
        type="text" 
        placeholder="Localisation" 
        class="border rounded p-2 w-full" 
        required
      />
    </div>

    <textarea 
      v-model="description" 
      placeholder="Description détaillée du problème" 
      class="border rounded p-2 w-full h-28 mb-4" 
      required
    ></textarea>

    <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
      <input
        type="file"
        accept="image/*"
        @change="onFileChange"
        class="block"
      />
      <button 
        @click="openCameraModal" 
        class="bg-green-600 text-white px-4 py-2 rounded shadow hover:bg-green-700"
      >
        Prendre une photo
      </button>
    </div>

    <div v-if="file" class="mb-4 text-sm text-green-600">
      ✓ Photo sélectionnée : {{ file.name }}
    </div>

    <button
      @click="submitSignalement"
      :disabled="loading || !objet || !localisation || !description || !file"
      :class="[
        'px-6 py-2 rounded shadow',
        loading || !objet || !localisation || !description || !file
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-green-700 hover:bg-green-800 text-white'
      ]"
    >
      {{ loading ? 'Envoi en cours...' : 'Envoyer le signalement' }}
    </button>
  </div>

  <!-- Mes signalements -->
  <div class="bg-white rounded-lg shadow">
    <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg">
      Mes signalements ({{ mesSignalements.length }})
    </div>
    <div class="p-4 bg-gray-50 overflow-x-auto">
      <table class="w-full text-left border border-collapse">
        <thead class="bg-green-100">
          <tr>
            <th class="p-2 border">Objet</th>
            <th class="p-2 border">Type</th>
            <th class="p-2 border">Date</th>
            <th class="p-2 border">Statut</th>
            <th class="p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in mesSignalements" :key="s.id" class="bg-white hover:bg-gray-50">
            <td class="p-2 border">{{ s.objet }}</td>
            <td class="p-2 border capitalize">{{ s.type_signalement_display }}</td>
            <td class="p-2 border">{{ formatDate(s.date_signalement) }}</td>
            <td class="p-2 border">
              <span :class="statusClass(s.statut)">
                {{ s.statut_display }}
              </span>
            </td>
            <td class="p-2 border">
              <button @click="voirDetails(s)"
                class="bg-blue-500 text-white px-2 py-1 rounded text-xs mr-1 hover:bg-blue-600">
                Détails
              </button>
              <button @click="supprimerSignalement(s.id)"
                class="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600">
                Supprimer
              </button>
            </td>
          </tr>
          <tr v-if="mesSignalements.length === 0">
            <td colspan="5" class="p-4 text-center text-gray-500">Aucun signalement trouvé.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Modal Caméra -->
  <div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-75 flex flex-col items-center justify-center z-50 p-4">
    <video ref="video" autoplay playsinline class="rounded shadow-lg max-w-full max-h-[60vh]"></video>
    <div class="mt-4 flex gap-4">
      <button 
        @click="capturePhoto" 
        class="bg-green-700 text-white px-4 py-2 rounded shadow hover:bg-green-800"
      >
        Prendre la photo
      </button>
      <button 
        @click="closeCameraModal" 
        class="bg-red-600 text-white px-4 py-2 rounded shadow hover:bg-red-700"
      >
        Annuler
      </button>
    </div>
    <canvas ref="canvas" class="hidden"></canvas>
  </div>

  <!-- Modal Détails -->
  <div v-if="showDetails && selectedSignalement" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-start mb-4">
        <h3 class="text-xl font-semibold">Détails du signalement</h3>
        <button @click="showDetails = false" class="text-gray-500 hover:text-gray-700">✕</button>
      </div>
      
      <div class="space-y-3">
        <div><strong>Objet :</strong> {{ selectedSignalement.objet }}</div>
        <div><strong>Type :</strong> {{ selectedSignalement.type_signalement_display }}</div>
        <div><strong>Description :</strong> {{ selectedSignalement.description }}</div>
        <div><strong>Localisation :</strong> {{ selectedSignalement.localisation }}</div>
        <div><strong>Statut :</strong> 
          <span :class="statusClass(selectedSignalement.statut)">
            {{ selectedSignalement.statut_display }}
          </span>
        </div>
        <div><strong>Date de signalement :</strong> {{ formatDate(selectedSignalement.date_signalement) }}</div>
        <div v-if="selectedSignalement.date_resolution">
          <strong>Date de résolution :</strong> {{ formatDate(selectedSignalement.date_resolution) }}
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

// Voir les détails
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
    case 'en_cours': return 'text-yellow-600 font-semibold'
    case 'traite': return 'text-green-600 font-semibold'
    case 'en_attente': return 'text-gray-600 font-semibold'
    default: return 'text-gray-600'
  }
}

// Initialisation
onMounted(async () => {
  await chargerChoix()
  await chargerMesSignalements()
})
</script>
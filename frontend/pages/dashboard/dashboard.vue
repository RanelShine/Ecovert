<template>
  <div class="max-w-4xl mx-auto py-8 px-4">
    <!-- FORMULAIRE -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <h2 class="text-2xl font-semibold text-green-700 mb-4">Faire un signalement</h2>

      <div class="flex gap-2 mb-4">
        <button
          v-for="type in ['pollution', 'déchets', 'climat']"
          :key="type"
          @click="selectedType = type"
          :class="[
            'px-4 py-2 rounded shadow',
            selectedType === type
              ? 'bg-green-700 text-white'
              : 'bg-green-100 text-green-800'
          ]"
        >
          {{ type }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <input v-model="objet" type="text" placeholder="Objet" class="border rounded p-2 w-full" />
        <input v-model="localisation" type="text" placeholder="Localisation" class="border rounded p-2 w-full" />
      </div>

      <textarea v-model="description" placeholder="Description" class="border rounded p-2 w-full h-28 mb-4"></textarea>

      <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
        <input
          type="file"
          accept="image/*"
          @change="onFileChange"
          class="block"
        />

        <button @click="openCameraModal" class="bg-green-600 text-white px-4 py-2 rounded shadow">
          Prendre une photo
        </button>
      </div>

      <button
        @click="submitData"
        class="bg-green-700 text-white px-6 py-2 rounded shadow hover:bg-green-800"
      >
        Envoyer le signalement
      </button>
    </div>

    <!-- TABLEAU -->
    <div class="border rounded-lg shadow">
      <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg">
        Liste de mes signalements
      </div>
      <div class="p-4 bg-gray-50 overflow-x-auto">
        <table class="w-full text-left border border-collapse">
          <thead class="bg-green-100">
            <tr>
              <th class="p-2 border">Objet</th>
              <th class="p-2 border">Type</th>
              <th class="p-2 border">Date</th>
              <th class="p-2 border">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in signalements" :key="s.id" class="bg-white hover:bg-gray-50">
              <td class="p-2 border">{{ s.objet }}</td>
              <td class="p-2 border capitalize">{{ s.type_signalement }}</td>
              <td class="p-2 border">{{ formatDate(s.date_signalement) }}</td>
              <td class="p-2 border">
                <span :class="statusClass(s.statut)">
                  {{ s.statut }}
                </span>
              </td>
            </tr>
            <tr v-if="signalements.length === 0">
              <td colspan="4" class="p-4 text-center text-gray-500">Aucun signalement trouvé.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL CAMERA -->
    <div v-if="showCamera" class="fixed inset-0 bg-black bg-opacity-75 flex flex-col items-center justify-center z-50 p-4">
      <video ref="video" autoplay playsinline class="rounded shadow-lg max-w-full max-h-[60vh]"></video>
      <div class="mt-4 flex gap-4">
        <button @click="capturePhoto" class="bg-green-700 text-white px-4 py-2 rounded shadow">Prendre la photo</button>
        <button @click="closeCameraModal" class="bg-red-600 text-white px-4 py-2 rounded shadow">Annuler</button>
      </div>
      <canvas ref="canvas" class="hidden"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
 definePageMeta({
    layout: 'dashboard'
  })
import { ref, onMounted, nextTick } from 'vue'

interface Signalement {
  id: number
  objet: string
  type_signalement: string
  date_signalement: string
  statut: string
}

const selectedType = ref('pollution')
const objet = ref('')
const localisation = ref('')
const description = ref('')
const file = ref<File | null>(null)
const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

const signalements = ref<Signalement[]>([])

const showCamera = ref(false)
const video = ref<HTMLVideoElement | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)
let stream: MediaStream | null = null

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
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false })
      if (video.value) {
        video.value.srcObject = stream
        await video.value.play()
      }
    } catch {
      alert('Impossible d\'accéder à la caméra.')
      showCamera.value = false
    }
  } else {
    alert('Votre navigateur ne supporte pas la capture vidéo.')
    showCamera.value = false
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

const fetchSignalements = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/signalements/liste/')
    if (!res.ok) throw new Error('Erreur lors du chargement des signalements')
    const data = await res.json()
    signalements.value = data
  } catch (error) {
    console.error(error)
  }
}

const submitData = async () => {
  if (!file.value) {
    alert('Veuillez prendre ou importer une photo.')
    return
  }

  try {
    const photoFormData = new FormData()
    photoFormData.append('image', file.value)
    if (latitude.value !== null) photoFormData.append('latitude', latitude.value.toString())
    if (longitude.value !== null) photoFormData.append('longitude', longitude.value.toString())

    const token = localStorage.getItem('authToken') || ''

  const photoResponse = await fetch('http://localhost:8000/api/photos/upload-photo/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: photoFormData,
    credentials: 'include'
  })


    if (!photoResponse.ok) throw new Error('Erreur lors de l\'upload de la photo')

    const photoData = await photoResponse.json()

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
    body: JSON.stringify(signalementPayload),
    credentials: 'include'
  })

    if (!response.ok) throw new Error('Erreur lors de la création du signalement')

    alert('Signalement envoyé avec succès !')
    fetchSignalements()
  } catch (error) {
    alert(error)
  }
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString()
}

const statusClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'en cours': return 'text-yellow-600'
    case 'résolu': return 'text-green-600'
    default: return 'text-gray-600'
  }
}

onMounted(fetchSignalements)
</script>

<style scoped>

</style>

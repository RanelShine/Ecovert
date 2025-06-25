<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-xl mx-auto bg-white p-6 rounded-lg shadow">
      <h2 class="text-2xl font-bold text-center text-green-600 mb-6">Formulaire de signalement</h2>

      <form @submit.prevent="soumettreFormulaire" class="space-y-4">
        <!-- Vidéo pour prévisualisation caméra -->
        <div>
          <label class="block text-gray-700 font-semibold mb-2">Prendre une photo</label>
          <div class="relative">
            <video
              ref="videoRef"
              autoplay
              playsinline
              class="w-full rounded border border-gray-300"
            ></video>
            <button
              type="button"
              @click="prendrePhoto"
              class="absolute bottom-2 right-2 bg-green-600 text-white px-4 py-1 rounded shadow"
            >
              Capturer
            </button>
          </div>
        </div>

        <!-- Affichage de la photo capturée -->
        <div v-if="photo">
          <label class="block text-gray-700 font-semibold mb-2 mt-4">Photo Capturée</label>
          <img :src="photo" class="w-full rounded border border-gray-300" />
        </div>

        <!-- Champ nom -->
        <div>
          <label class="block text-gray-700 font-semibold mb-2">Nom</label>
          <input
            v-model="form.nom"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Entrez votre nom"
          />
        </div>

        <!-- Champ objet -->
        <div>
          <label class="block text-gray-700 font-semibold mb-2">Objet</label>
          <input
            v-model="form.objet"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Entrez l'objet"
          />
        </div>

        <!-- Champ description -->
        <div>
          <label class="block text-gray-700 font-semibold mb-2">Description</label>
          <textarea
            v-model="form.description"
            rows="4"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Entrez une description"
          ></textarea>
        </div>

        <!-- Soumission -->
        <div class="text-center mt-6">
          <button
            type="submit"
            class="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded"
          >
            Soumettre
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const form = ref({
  nom: '',
  objet: '',
  description: '',
})

const videoRef = ref<HTMLVideoElement | null>(null)
const photo = ref<string | null>(null)
let stream: MediaStream | null = null

const initCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
  } catch (err) {
    alert('Accès à la caméra refusé ou non disponible.')
  }
}

const prendrePhoto = () => {
  if (!videoRef.value) return

  const canvas = document.createElement('canvas')
  canvas.width = videoRef.value.videoWidth
  canvas.height = videoRef.value.videoHeight
  const context = canvas.getContext('2d')
  if (context) {
    context.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height)
    photo.value = canvas.toDataURL('image/png')
  }
}

const soumettreFormulaire = () => {
  // Simulation d'envoi
  console.log('Formulaire soumis avec les données :', form.value)
  console.log('Photo capturée :', photo.value)
  alert('Formulaire soumis avec succès !')
}

onMounted(() => {
  initCamera()
})

onUnmounted(() => {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop())
  }
})
</script>

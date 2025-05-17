<template>
  <div>
    <!-- Carte de signalement seule -->
    <div class="border rounded-lg shadow mb-6">
      <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
        <span>faire un signalement</span>
        <span class="text-xl">svg</span>
      </div>
      <div class="flex flex-wrap gap-4 bg-gray-200 p-4 rounded-b-lg">
        <div class="bg-gray-100 p-4 rounded shadow">
          <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            déchets
          </NuxtLink>
        </div>
        <div class="bg-gray-100 p-4 rounded shadow">
          <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            pollution
          </NuxtLink>
        </div>
        <div class="bg-gray-100 p-4 rounded shadow">
          <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            écologie
          </NuxtLink>
        </div>
        <div class="bg-gray-100 p-4 rounded shadow">
          <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            dégradations
          </NuxtLink>
        </div>
      </div>
      <div class="flex justify-center bg-gray-100 p-6">
  <form class="w-full max-w-xl" @submit.prevent="ajout">
    <div class="relative">
      <!-- objet -->
      <input
        id="objet"
        name="objet"
        type="text"
        autocomplete="objet"
        required
        v-model="objet"
        class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
        placeholder="ajouter l'objet du signalement"
      />
    </div>
<!-- localisation -->
 <div class="relative">
    <input
        id="localisation"
        name="localisation"
        type="text"
        autocomplete="localisation"
        required
        v-model="objet"
        class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
        placeholder="ajouter l'emplacement du siglement"
      />
    </div>
    <!-- description -->
    <div class="relative">
      <textarea
        id="description"
        name="description"
        type="text"
        required
        v-model="description"
        class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
        placeholder="ajouter une description"
      ></textarea>
    </div>

    <!-- photo -->
    <div class="relative">
      <input
        id="file"
        name="file"
        type="file"
        required
        class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
      />
    </div>
    <div class="relative">
    <video ref="video" autoplay playsinline></video>
    <button @click="takePhoto">Prendre une photo</button>
    <canvas ref="canvas" style="display: none;"></canvas>
    <form @submit.prevent="submitData">
      <input type="hidden" v-model="latitude" />
      <input type="hidden" v-model="longitude" />
      <input type="submit" class="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        :disabled="loading" value="Envoyer" />
    </form>
  </div>

    <!-- Bouton
    <div>
      <button
        type="submit"
        class="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        :disabled="loading"
      >
        <span v-if="loading">Chargement...</span>
        <span v-else>Ajouter</span>
      </button>
    </div> -->

    <!-- Erreur -->
    <div v-if="error" class="text-red-600 text-center mt-4">
      {{ error }}
    </div>
  </form>
</div>

    </div>

      <!-- Carte de liste de signalement -->
      <div class="border rounded-lg shadow">
        <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
          <span>Liste des signalements</span>
          <span class="text-xl">svg</span>
        </div>
        <div class="bg-gray-100 p-4 rounded-b-lg space-y-4">
          <!-- definition des elements pour la liste des signalements -->
        </div>
      </div>

      <!-- Carte 3 -->
       <div class="flex pt-4 gap-4">
      <div class="border rounded-lg shadow">
        <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
          <span>autre carte</span>
          <span class="text-xl"> </span>
        </div>
        <div class="bg-gray-100 p-4 rounded-b-lg space-y-4">
          <!-- definition des elements pour cette carte -->
        </div>
      </div>
      <div class="border rounded-lg shadow">
        <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
          <span>autre carte</span>
          <span class="text-xl"> </span>
        </div>
        <div class="bg-gray-100 p-4 rounded-b-lg space-y-4">
          <!-- definition des elements pour cette carte -->
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
definePageMeta({
  layout: 'dashboard'
})

import { ref, onMounted } from 'vue'

const video = ref(null)
const canvas = ref(null)
const latitude = ref('')
const longitude = ref('')
let photoBlob = null

onMounted(async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    video.value.srcObject = stream
  } catch (err) {
    alert("Erreur d'accès à la caméra : " + err)
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      latitude.value = pos.coords.latitude
      longitude.value = pos.coords.longitude
    },
    (err) => {
      alert("Erreur GPS : " + err.message)
    }
  )
})

const takePhoto = () => {
  const context = canvas.value.getContext('2d')
  canvas.value.width = video.value.videoWidth
  canvas.value.height = video.value.videoHeight
  context.drawImage(video.value, 0, 0)
  canvas.value.toBlob((blob) => {
    photoBlob = blob
  }, 'image/jpeg')
}

const submitData = async () => {
  if (!photoBlob) {
    alert('Prenez d’abord une photo.')
    return
  }

  const formData = new FormData()
  formData.append('image', photoBlob, 'photo.jpg')
  formData.append('latitude', latitude.value)
  formData.append('longitude', longitude.value)

  await fetch('http://localhost:8000/api/photos/upload-photo/', {
    method: 'POST',
    body: formData
  })
  alert("Données envoyées !")
}

const user = useState('user')
</script>
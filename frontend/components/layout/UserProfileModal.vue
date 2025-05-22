<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Profil de l'utilisateur</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-800">&times;</button>
      </div>
      <div v-if="user">
        <p><strong>Nom :</strong> {{ user.nom }}</p>
        <p><strong>Email :</strong> {{ user.email }}</p>
        <p><strong>Prénom :</strong> {{ user.prenom }}</p>
        <p><strong>Téléphone :</strong> {{ user.telephone }}</p>
        <p><strong>Commune :</strong> {{ user.commune?.nom || 'Non renseignée' }}</p>
      </div>
      <div v-else>
        <p>Chargement du profil...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  visible: Boolean
})

// État local pour stocker le profil utilisateur
const user = ref(null)

// Charger l'utilisateur quand la fenêtre devient visible
watch(() => props.visible, async (isVisible) => {
  if (isVisible) {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/accounts/me/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Remplace ce token par la récupération réelle (par ex. depuis le store ou localStorage)
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        credentials: 'include' // Si tu utilises session/cookies, garde cette ligne
      })

      if (!response.ok) {
        throw new Error('Erreur de récupération du profil')
      }

      user.value = await response.json()
    } catch (error) {
      console.error(error)
      user.value = null
    }
  }
})
</script>

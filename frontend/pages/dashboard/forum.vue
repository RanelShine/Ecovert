<!-- pages/forum.vue -->
<template>
  <div class="max-w-6xl mx-auto py-8 px-4">
    <ForumSection v-if="user" :current-user="user" />
    <div v-else class="text-center py-8">
      <p class="text-gray-600">Chargement...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ForumSection from '@/components/sections/forums/ForumSection.vue'

interface User {
  id: number;
  email: string;
  nom: string;
  prenom: string;
  telephone?: string;
  role: string;
  commune?: number;
  is_active: boolean;
  is_verified: boolean;
}

definePageMeta({
  layout: 'dashboard'
})

const user = ref<User | null>(null)

onMounted(async () => {
  try {
    const token = localStorage.getItem('authToken')
    if (token) {
      const response = await fetch('http://localhost:8000/api/accounts/me/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      if (response.ok) {
        user.value = await response.json()
      } else {
        console.error('Erreur lors de la récupération de l\'utilisateur')
      }
    }
  } catch (error) {
    console.error('Erreur:', error)
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto py-8 px-4">
    <!-- En-tête avec bouton -->
    <div v-if="userRole === 'ctd'" class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Projets de la commune</h1>
      <a href="#nouveau-projet"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
        <span class="mr-2">+</span>
        Nouveau projet
      </a>
    </div>

    <!-- Section CTD -->
    <div v-if="userRole === 'ctd'" id="nouveau-projet">
      <CTDProjetSection />
    </div>

    <!-- Section Citoyens -->
    <div v-if="userRole === 'citoyen'">
      <CitoyenProjetSection />
    </div>

    <!-- Section ONG/Entreprise -->
    <div v-if="userRole === 'ong' || userRole === 'entreprise'">
      <EntrepriseProjetSection />
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})

import { ref, onMounted } from 'vue'
import CTDProjetSection from '~/components/sections/projets/CTDProjetSection.vue'
import CitoyenProjetSection from '~/components/sections/projets/CitoyenProjetSection.vue'
import EntrepriseProjetSection from '~/components/sections/projets/EntrepriseProjetSection.vue'

const userRole = ref<string>('')

// Fonction pour récupérer le rôle utilisateur
const getUserRole = () => {
  const userRole = localStorage.getItem('userRole')
  if (userRole) {
    return userRole.toLowerCase()
  }
  return 'citoyen'
}

onMounted(() => {
  userRole.value = getUserRole()
})
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}
</style>
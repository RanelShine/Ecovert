<template>
  <div class="max-w-6xl mx-auto py-8 px-4">
    <!-- Section CTD -->
    <div v-if="userRole === 'CTD'">
      <CTDProjetSection />
    </div>
    
    <!-- Section Citoyens -->
    <div v-if="userRole === 'citoyen'">
      <CitoyenProjetSection />
    </div>
    
    <!-- Section ONG/Entreprise -->
    <div v-if="userRole === 'ONG' || userRole === 'entreprise'">
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
  const userData = localStorage.getItem('userData')
  if (userData) {
    const user = JSON.parse(userData)
    return user.role || 'citoyen'
  }
  return 'citoyen'
}

onMounted(() => {
  userRole.value = getUserRole()
})
</script>
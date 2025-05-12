<template>
    <header class="bg-white shadow px-4 py-2 flex justify-between items-center">
      <div class="flex items-center space-x-4">
        <h1 class="flex items-center text-lg font-semibold text-green-800">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="mr-2">
            <path fill="currentColor" d="M3 13h8V3H3zm0 8h8v-6H3zm10 0h8V11h-8zm0-18v6h8V3z"/>
          </svg>
          Tableau de bord
        </h1>
        <input
          type="text"
          placeholder="Rechercher..."
          class="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring focus:border-blue-300"
        />
      </div>
  
      <div>
        <template v-if="isAuthenticated">
  <div class="relative">
    <button @click="toggleDropdown" class="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">
      
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4s-4 1.79-4 4s1.79 4 4 4m0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/>
          </svg>
      <span>{{ user?.nom || 'Utilisateur' }}</span>
    </button>

    <div
      v-if="showDropdown"
      class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10"
    >
      <div class="py-1">
        <button
      @click="showProfile = true"
      class="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
    >
      Voir Profil
    </button>

    <UserProfileModal :visible="showProfile" :user="user" @close="showProfile = false" />
        <button @click="logout" class="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
          Déconnexion
        </button>
      </div>
    </div>
  </div>
</template>

              <template v-else>
                <NuxtLink to="/auth/login" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">Connexion</NuxtLink>
                <NuxtLink to="/auth/register" class="ml-2 px-3 py-2 rounded-md text-sm font-medium bg-green-600 text-white hover:bg-green-700">Inscription</NuxtLink>
              </template>
      </div>
    </header>
  </template>
 <script setup>
 import { useAuthStore } from '~/stores/auth'
 import { storeToRefs } from 'pinia'
 import { ref, onMounted } from 'vue'
 import { useRouter } from 'vue-router'
 import UserProfileModal from '~/components/layout/UserProfileModal.vue'

const showProfile = ref(false)
 
 const authStore = useAuthStore()
 const { isAuthenticated, user } = storeToRefs(authStore)
 const router = useRouter()
 const showDropdown = ref(false)
 
 onMounted(() => {
   authStore.initAuth()
 })
 
 function toggleDropdown() {
   showDropdown.value = !showDropdown.value
 }
 
 const logout = async () => {
   await authStore.logout()
   router.push('/auth/login')
 }
 </script>
 
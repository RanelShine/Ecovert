<template>
  <div class="flex flex-col min-h-screen">
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo et navigation principale -->
          <div class="flex items-center">
            <NuxtLink to="/" class="flex-shrink-0 flex items-center">
              <span class="text-green-600 text-xl font-bold">EcoVert</span>
            </NuxtLink>
            
            <!-- Navigation des pages publiques -->
            <nav class="ml-8 flex items-center space-x-6">
              <a href="http://www.cipcre.org" class="text-gray-500 hover:text-gray-700 text-sm font-medium">
                À propos
              </a>
              <NuxtLink to="/contact" class="text-gray-500 hover:text-gray-700 text-sm font-medium">  
                Contact
              </NuxtLink>
            </nav>
            
            <!-- Navigation pour utilisateurs connectés -->
            <nav class="ml-6 flex items-center" v-if="isAuthenticated">
              <NuxtLink to="/dashboard/dashboard" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
                Tableau de bord
              </NuxtLink>
            </nav>
          </div>

          <!-- Menu utilisateur / Authentification -->
          <div class="flex items-center">
            <!-- Menu utilisateur connecté -->
            <template v-if="isAuthenticated">
              <div class="relative">
                <button @click="toggleDropdown" class="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
                  <span>{{ user?.nom || 'Utilisateur' }}</span>
                  <svg class="ml-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div
                  v-if="showDropdown"
                  class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10"
                >
                  <div class="py-1">
                    <NuxtLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Profil
                    </NuxtLink>
                    <button @click="logout" class="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Déconnexion
                    </button>
                  </div>
                </div>
              </div>
            </template>
            
            <!-- Boutons pour utilisateurs non connectés -->
            <template v-else>
              <div class="flex items-center space-x-2">
                <NuxtLink to="/auth/login" class="px-4 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
                  Connexion
                </NuxtLink>
                <NuxtLink to="/auth/register" class="px-4 py-2 rounded-md text-sm font-medium bg-green-600 text-white hover:bg-green-700 transition-colors">
                  Inscription
                </NuxtLink>
              </div>
            </template>
          </div>
        </div>
      </div>
    </header>
  
      <main class="flex-grow">
        <div class=" mx-auto sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
  
      <footer class="bg-white border-t border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div class="flex justify-between items-center">
            <div>
              <p class="text-sm text-gray-500">&copy; {{ new Date().getFullYear() }} Redevabilité Verte. Tous droits réservés.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </template>
  
  <script setup>
   import { useAuthStore } from '~/stores/auth'
   import { storeToRefs } from 'pinia'
   import { ref } from 'vue'

const showDropdown = ref(false)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}
   const authStore = useAuthStore()
   const { isAuthenticated, user } = storeToRefs(authStore)
   
   const router = useRouter()
   
   const logout = async () => {
     await authStore.logout()
     router.push('/auth/login')
   }
   </script>
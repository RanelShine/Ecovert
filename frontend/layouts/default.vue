<template>
    <div class="flex flex-col min-h-screen">
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex">
              <NuxtLink to="/" class="flex-shrink-0 flex items-center">
                <span class="text-green-600 text-xl font-bold">Redevabilité Verte</span>
              </NuxtLink>
              <nav class="ml-8 flex items-center space-x-4" v-if="isAuthenticated">
                <NuxtLink to="/" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">Accueil</NuxtLink>
                <NuxtLink to="/dashboard/dashboard" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">Tableau de bord</NuxtLink>
              </nav>
            </div>
            <div class="flex items-center">
              <template v-if="isAuthenticated">
                <div class="relative group">
                  <button class="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">
                    <span>{{ user?.nom || 'Utilisateur' }}</span>
                    <svg class="ml-1 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <div class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 hidden group-hover:block z-10">
                    <div class="py-1">
                      <NuxtLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profil</NuxtLink>
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
            <div class="flex space-x-6">
              <a href="#" class="text-gray-500 hover:text-gray-700">
                <span class="sr-only">À propos</span>
                À propos
              </a>
            <NuxtLink to="/contact" class="text-gray-500 hover:text-gray-700">  
                <span class="sr-only">Contact</span>
                Contact
              </NuxtLink>
              <a href="#" class="text-gray-500 hover:text-gray-700">
                <span class="sr-only">Mentions légales</span>
                Mentions légales
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </template>
  
  <script setup>
  import { useAuthStore } from '~/stores/auth'
  import { storeToRefs } from 'pinia'
  
  const authStore = useAuthStore()
  const { isAuthenticated, user } = storeToRefs(authStore)
  
  const router = useRouter()
  
  const logout = async () => {
    await authStore.logout()
    router.push('/auth/login')
  }
  </script>
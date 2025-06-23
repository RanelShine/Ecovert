<template>
  <div class="flex">
    <!-- Bouton hamburger (visible uniquement sur petits écrans) -->
    <button class="sm:hidden fixed top-4 left-4 z-50 p-2 bg-green-700 text-white rounded-md shadow-lg" @click="toggleSidebar">
      <!-- Icône hamburger ou X selon l'état -->
      <svg v-if="!isSidebarOpen" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    </button>

    <!-- Overlay qui ferme la sidebar -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-30 sm:hidden"
      @click="toggleSidebar"
    ></div>

    <!-- Sidebar responsive -->
    <aside
      :class="[
        // Classes de base
        'bg-green-700 dark:bg-gray-900 dark:text-green-600 text-white p-4 space-y-4 transition-all duration-300 ease-in-out',
        // Mobile: position fixe, taille réduite, en haut à gauche
        'fixed sm:static w-72 sm:w-64',
        // Mobile: positionnement et hauteur
        'top-4 left-4 sm:top-0 sm:left-0',
        'max-h-[70vh] sm:min-h-screen', // Hauteur limitée sur mobile, pleine hauteur sur desktop
        'rounded-lg sm:rounded-none', // Coins arrondis sur mobile
        'shadow-2xl sm:shadow-none', // Ombre sur mobile
        'overflow-y-auto', // Scroll si contenu trop long
        'z-40',
        // Animation de transition
        isSidebarOpen ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0 sm:translate-x-0 sm:opacity-100'
      ]"
    >
      <!-- Header avec bouton fermer sur mobile -->
      <div class="flex items-center justify-between mb-4 sm:mb-0">
        <!-- Logo -->
        <NuxtLink to="/" class="flex-shrink-0 flex items-center" @click="closeSidebarOnMobile">
          <span class="text-xl font-bold">EcoVert</span>
        </NuxtLink>
        
        <!-- Bouton fermer (visible uniquement sur mobile) -->
        <button 
          class="sm:hidden p-1 hover:bg-green-600 rounded transition-colors"
          @click="toggleSidebar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Menu de navigation -->
      <nav class="space-y-1">
        <ul class="space-y-1">
          <li>
            <NuxtLink 
              to="/dashboard/dashboard" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700 transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                <path fill="currentColor" d="M1 21h22L12 2zm12-3h-2v-2h2zm0-4h-2v-4h2z"/>
              </svg>
              Signalements
            </NuxtLink>
          </li>

          <li>
            <NuxtLink 
              to="/dashboard/forum" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700  transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20 6h-1v8c0 .55-.45 1-1 1H6v1c0 1.1.9 2 2 2h10l4 4V8c0-1.1-.9-2-2-2m-3 5V4c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v13l4-4h9c1.1 0 2-.9 2-2"/>
              </svg>
              Forum
            </NuxtLink>
          </li>

          <li>
            <NuxtLink 
              to="/dashboard/projects" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700 transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                <path fill="currentColor" d="M3 6H1v13c0 1.1.9 2 2 2h17v-2H3z"/>
                <path fill="currentColor" d="M21 4h-7l-2-2H7c-1.1 0-1.99.9-1.99 2L5 15c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2"/>
              </svg>
              Projets
            </NuxtLink>
          </li>

          <li>
            <NuxtLink 
              to="/dashboard/meteo" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700 transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                <path fill="currentColor" d="M18.16 17.98c-2.76 1.76-4.67.77-5.61.08a.96.96 0 0 0-1.12.01c-.97.7-2.83 1.65-5.55-.06c-.33-.21-.75-.23-1.07-.01c-.91.61-1.53.85-2 .94s-.81.5-.81.97c0 .6.54 1.09 1.13.98c.77-.14 1.51-.42 2.2-.83a6.58 6.58 0 0 0 6.67 0a6.54 6.54 0 0 0 6.67 0c.69.41 1.44.69 2.21.83c.59.11 1.13-.38 1.13-.98v-.01c0-.47-.33-.88-.8-.97c-.49-.1-1.11-.34-2.02-.94a.96.96 0 0 0-1.03-.01M19.33 12H21c.55 0 1-.45 1-1s-.45-1-1-1h-1.61c-1.86 0-3.4-1.5-3.39-3.36c0-.37.06-.7.16-1.05c.37-1.29-.56-2.56-1.89-2.59H14C7.36 3 2.15 8.03 2.01 14.5v.03c-.04 1.13 1.07 1.98 2.14 1.6c.4-.14.78-.32 1.15-.54c2.08 1.2 4.64 1.22 6.7-.02a6.54 6.54 0 0 0 6.67 0c.68.41 1.42.68 2.18.82a.99.99 0 0 0 1.16-.98v-.01c0-.46-.32-.88-.78-.97c-.49-.09-1.12-.33-2.03-.94a.95.95 0 0 0-1.05-.01c-2.73 1.74-4.63.77-5.58.09a.99.99 0 0 0-1.16-.01c-.15.11-.09.06-.32.2c-.7-.94-1.09-2.06-1.09-3.26c0-2.58 1.77-4.74 4.21-5.33c-.13.51-.21 1.02-.21 1.5C14 9.61 16.39 12 19.33 12"/>
              </svg>
              Météo
            </NuxtLink>
          </li>

          <li>
            <NuxtLink 
              to="/dashboard/cartographie" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700 transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                <path fill="currentColor" d="m20.5 3l-.16.03L15 5.1L9 3L3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1l5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5M15 19l-6-2.11V5l6 2.11z"/>
              </svg>
              Cartographie
            </NuxtLink>
          </li>

          <li>
            <NuxtLink 
              to="/dashboard/notifications" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700  transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M7.58 4.08L6.15 2.65C3.75 4.48 2.17 7.3 2.03 10.5h2a8.45 8.45 0 0 1 3.55-6.42m12.39 6.42h2c-.15-3.2-1.73-6.02-4.12-7.85l-1.42 1.43a8.5 8.5 0 0 1 3.54 6.42M18 11c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-6 11c.14 0 .27-.01.4-.04c.65-.14 1.18-.58 1.44-1.18q.15-.36.15-.78h-4c.01 1.1.9 2 2.01 2"/>
              </svg>
              Notifications
            </NuxtLink>
          </li>

          <li>
            <NuxtLink 
              to="/dashboard/chatbot" 
              class="flex items-center gap-3 py-3 px-3 rounded-lg hover:bg-green-600 dark:hover:bg-gray-700 transition-colors duration-200 text-sm" 
              exact-active-class="bg-green-800"
              @click="closeSidebarOnMobile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                <path fill="currentColor" d="M15.85 8.14c.39 0 .77.03 1.14.08C16.31 5.25 13.19 3 9.44 3c-4.25 0-7.7 2.88-7.7 6.43c0 2.05 1.15 3.86 2.94 5.04L3.67 16.5l2.76-1.19c.59.21 1.21.38 1.87.47c-.09-.39-.14-.79-.14-1.21c-.01-3.54 3.44-6.43 7.69-6.43M12 5.89a.96.96 0 1 1 0 1.92a.96.96 0 0 1 0-1.92M6.87 7.82a.96.96 0 1 1 0-1.92a.96.96 0 0 1 0 1.92"/>
                <path fill="currentColor" d="M22.26 14.57c0-2.84-2.87-5.14-6.41-5.14s-6.41 2.3-6.41 5.14s2.87 5.14 6.41 5.14c.58 0 1.14-.08 1.67-.2L20.98 21l-1.2-2.4c1.5-.94 2.48-2.38 2.48-4.03m-8.34-.32a.96.96 0 1 1 .96-.96c.01.53-.43.96-.96.96m3.85 0a.96.96 0 1 1 0-1.92a.96.96 0 0 1 0 1.92"/>
              </svg>
              Chatbot
            </NuxtLink>
          </li>
        </ul>
      </nav>
    </aside>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isSidebarOpen = ref(false)

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

function closeSidebarOnMobile() {
  // Fermer la sidebar seulement sur mobile après navigation
  if (window.innerWidth < 640) {
    isSidebarOpen.value = false
  }
}
</script>

<style scoped>
/* Amélioration de l'apparence sur mobile */
@media (max-width: 640px) {
  aside {
    /* Bordure subtile pour distinguer du fond */
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  /* Animation plus fluide */
  .transition-all {
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
}

/* Scroll personnalisé pour la sidebar */
aside::-webkit-scrollbar {
  width: 4px;
}

aside::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

aside::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

aside::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
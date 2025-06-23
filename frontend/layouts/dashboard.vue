<template>
    <div class="flex h-screen overflow-hidden">
      <Sidebar />
  
      <div class="flex-1 flex flex-col">
        <Navbar />
        <main class="flex-1 overflow-auto bg-gray-100">
          <slot />
        </main>
        <Footer />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  // Import des composants depuis le bon dossier
  import Sidebar from '@/components/layout/Sidebar.vue'
  import Navbar from '@/components/layout/Navbar.vue'
  import Footer from '@/components/layout/Footer.vue'
  </script>
  
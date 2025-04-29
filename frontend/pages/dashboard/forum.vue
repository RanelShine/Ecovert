<template>
    <div>
      <h1 class="text-2xl font-bold text-green-700 mb-4">Bienvenue sur le forum</h1>
    </div>
  </template>
  
  <script setup lang="ts">
  definePageMeta({
    layout: 'dashboard'
  })
  
  const user = useState('user')
  </script>
  
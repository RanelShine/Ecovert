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
          <p><strong>Prenom :</strong> {{ user.prenom }}</p>
          <p><strong>Telephone :</strong> {{ user.telephone }}</p>
          <p><strong>Commune :</strong> {{ user.commune.nom }}</p>
        </div>
        <div v-else>
          <p>Erreur lors du chargement du profil...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    visible: Boolean,
    user: Object
  })
  </script>
  
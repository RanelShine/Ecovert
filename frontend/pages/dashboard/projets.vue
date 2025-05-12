<template>
    <div>

      <!-- Carte de liste de projet -->
      <div class="border mb-4 rounded-lg shadow">
          <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
            <span>Liste de projets</span>
            <span class="text-xl">svg</span>
          </div>
          <div class="bg-gray-100 p-4 rounded-b-lg space-y-4">
            <!-- definition des elements pour la liste des signalements -->
          </div>
        </div>

      <!-- Carte de demande de compte -->
      <div class="border rounded-lg shadow mb-6">
        <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
          <span>Demander des comptes par rapport a un projet</span>
          <span class="text-xl">svg</span>
        </div>
        <!-- <div class="flex flex-wrap gap-4 bg-gray-200 p-4 rounded-b-lg">
          <div class="bg-gray-100 p-4 rounded shadow">
            <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              déchets
            </NuxtLink>
          </div>
          <div class="bg-gray-100 p-4 rounded shadow">
            <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              pollution
            </NuxtLink>
          </div>
          <div class="bg-gray-100 p-4 rounded shadow">
            <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              écologie
            </NuxtLink>
          </div>
          <div class="bg-gray-100 p-4 rounded shadow">
            <NuxtLink to="/signalement" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              dégradations
            </NuxtLink>
          </div>
        </div> -->
        <div class="flex justify-center bg-gray-100 p-6">
    <form class="w-full max-w-xl" @submit.prevent="ajout">
      <!-- objet -->
    <div class="relative">
      <input
        id="objet"
        name="objet"
        type="text"
        autocomplete="objet"
        required
        v-model="objet"
        class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
        placeholder="ajouter de la demande"
      />
    </div>
      <!-- projets -->
      <div class="relative">
        <input
          id="projet"
          name="projet"
          type="text"
          autocomplete="projet"
          required
          v-model="projet"
          class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
          placeholder="liste de projets"
        />
      </div>
  
      <!-- description -->
      <div class="relative">
        <textarea
          id="description"
          name="description"
          type="text"
          required
          v-model="description"
          class="appearance-none mb-4 block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900"
          placeholder="ajouter une description"
        ></textarea>
      </div>
  
      <!-- Bouton -->
      <div>
        <button
          type="submit"
          class="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          :disabled="loading"
        >
          <span v-if="loading">Chargement...</span>
          <span v-else>Ajouter</span>
        </button>
      </div>
  
      <!-- Erreur -->
      <div v-if="error" class="text-red-600 text-center mt-4">
        {{ error }}
      </div>
    </form>
  </div>
  
      </div>
  
        <!-- Carte 3 -->
         <div class="flex pt-4 gap-4">
        <div class="border rounded-lg shadow">
          <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
            <span>autre carte</span>
            <span class="text-xl"> </span>
          </div>
          <div class="bg-gray-100 p-4 rounded-b-lg space-y-4">
            <!-- definition des elements pour cette carte -->
          </div>
        </div>
        <div class="border rounded-lg shadow">
          <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex items-center justify-between">
            <span>autre carte</span>
            <span class="text-xl"> </span>
          </div>
          <div class="bg-gray-100 p-4 rounded-b-lg space-y-4">
            <!-- definition des elements pour cette carte -->
          </div>
        </div>
      </div>
    </div>
  </template>
  <script setup lang="ts">
  definePageMeta({
    layout: 'dashboard'
  })
  
  const user = useState('user')
  </script>
  
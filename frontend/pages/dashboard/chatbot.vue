<script setup lang="ts">
 definePageMeta({
    layout: 'dashboard'
  })
const isRedevabiliteVerte = true // ou false pour test accès refusé

import { ref } from 'vue'

interface Message {
  from: 'user' | 'bot'
  text: string
}

const messages = ref<Message[]>([])

const userInput = ref('')

// Simuler réponse IA basique
function sendMessage() {
  if (!userInput.value.trim()) return

  messages.value.push({ from: 'user', text: userInput.value })

  // Simuler une réponse IA (ici on répète ce que l'utilisateur dit)
  setTimeout(() => {
    messages.value.push({ from: 'bot', text: "Réponse IA : " + userInput.value })
  }, 1000)

  userInput.value = ''
}
</script>

<template>
  <div class="max-w-xl mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Chatbot IA - Redevabilité Verte</h1>

    <div v-if="isRedevabiliteVerte">
      <div class="border rounded p-4 h-96 overflow-auto mb-4 flex flex-col gap-2">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="[
            'p-2 rounded max-w-[70%]',
            msg.from === 'user' ? 'self-end bg-green-600 text-white' : 'self-start bg-gray-200'
          ]"
        >
          {{ msg.text }}
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="flex gap-2">
        <input
          v-model="userInput"
          type="text"
          placeholder="Écris ton message..."
          class="flex-grow border rounded px-3 py-2"
        />
        <button type="submit" class="bg-green-600 text-white px-4 rounded">Envoyer</button>
      </form>
    </div>

    <div v-else class="text-center text-red-600 font-semibold">
      Accès refusé. Cette page est uniquement accessible pour la redevabilité verte.
    </div>
  </div>
</template>

<style scoped>
/* Ajoute un peu de style si besoin */
</style>

  <!-- <script setup lang="ts">
  definePageMeta({
    layout: 'dashboard'
  })
  
  const user = useState('user')
  </script> -->
  
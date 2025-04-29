<template>
  <div>
    <h1 class="text-2xl font-bold text-green-700 mb-6">Bienvenue sur votre tableau de bord</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(card, index) in cards"
        :key="index"
        class="border rounded-lg shadow"
      >
        <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg">
          {{ card.title }}
        </div>
        <div class="bg-gray-100 p-4 rounded-b-lg">
          {{ card.content }}
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

const cards = [
  { title: 'Carte 1', content: 'carte 1.' },
  { title: 'Carte 2', content: 'carte 2.' },
  { title: 'Carte 3', content: 'carte 3.' },
  { title: 'Carte 4', content: 'carte 4.' },
  { title: 'Carte 5', content: 'carte 5.' },
  { title: 'Carte 6', content: 'carte 6.' },
  { title: 'Carte 7', content: 'carte 7.' },
  { title: 'Carte 8', content: 'carte 8.' },
  { title: 'Carte 9', content: 'carte 9.' },
]
</script>

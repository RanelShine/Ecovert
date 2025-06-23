<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">Prévision météo (24h & semaine)</h2>
    
    <button @click="loadMyPosition" class="bg-green-600 text-white px-4 py-2 rounded mb-4">
      📍 Ma position
    </button>

    <div v-if="weatherStore.loading">Chargement...</div>
    <div v-else-if="weatherStore.error">{{ weatherStore.error }}</div>
    <div v-else-if="weatherStore.forecast">
      <h3 class="text-lg font-semibold mb-2">Aujourd’hui</h3>
      <p>{{ weatherStore.forecast.current.weather[0].description }}</p>
      <p>Température actuelle : {{ weatherStore.forecast.current.temp }}°C</p>

      <h3 class="text-lg font-semibold mt-4 mb-2">Semaine</h3>
      <ul>
        <li v-for="(day, i) in weatherStore.forecast.daily.slice(0, 7)" :key="i">
          {{ new Date(day.dt * 1000).toLocaleDateString() }} :
          {{ day.weather[0].description }}, {{ day.temp.day }}°C
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
  definePageMeta({
    layout: 'dashboard'
  })
import { useWeatherStore } from '@/stores/weather'
const weatherStore = useWeatherStore()

onMounted(() => {
  weatherStore.fetchGlobalWeather()
})

const loadMyPosition = () => {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      weatherStore.fetchWeatherByPosition(latitude, longitude)
    },
    (error) => {
      alert("Impossible d'obtenir votre position.")
    }
  )
}
</script>


  
import { defineStore } from 'pinia'

export const useWeatherStore = defineStore('weather', {
  state: () => ({
    forecast: null as any | null,
    loading: false,
    error: null as string | null
  }),
  actions: {
    async fetchGlobalWeather() {
      this.loading = true
      this.error = null
      try {
        const { data } = await useFetch('/api/weather')
        this.forecast = data.value
      } catch (err: any) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },

    async fetchWeatherByPosition(lat: number, lon: number) {
      this.loading = true
      this.error = null
      try {
        const { data } = await useFetch(`/api/weather/position?lat=${lat}&lon=${lon}`)
        this.forecast = data.value
      } catch (err: any) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    }
  }
})

// plugins/axios.ts
import axios from 'axios'
import { defineNuxtPlugin, useCookie } from '#imports'

export default defineNuxtPlugin(() => {
  // 1) Définir la baseURL vers votre API Django (ajustez si besoin)
  axios.defaults.baseURL = process.env.API_BASE_URL || 'http://localhost:8000'

  // 2) Inclure automatiquement le cookie de session (SessionAuthentication)
  axios.defaults.withCredentials = true

  // 3) Ou, si vous utilisez TokenAuthentication :
  //    const token = useCookie('userToken').value || localStorage.getItem('userToken')
  //    if (token) {
  //      axios.defaults.headers.common['Authorization'] = `Token ${token}`
  //    }

  return {
    provide: {
      axios
    }
  }
})

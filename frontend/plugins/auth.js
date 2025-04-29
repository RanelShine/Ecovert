import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(async (nuxtApp) => {
  const authStore = useAuthStore()
  
  // Initialiser l'authentification à partir du localStorage
  const isAuthenticated = authStore.initAuth()
  
  // Si authentifié, récupérer les infos utilisateur
  if (isAuthenticated) {
    await authStore.fetchCurrentUser()
  }

  // Middleware global via hook de navigation
  nuxtApp.hook('page:start', async (context) => {
    const route = useRoute()
    const requiresAuth = route.meta?.auth

    // Redirection si l'auth est requise mais non connecté
    if (requiresAuth && !authStore.isAuthenticated) {
      return await navigateTo('/auth/login')
    }

    // Redirection si connecté et tente d'accéder à une page auth
    if (route.path.startsWith('/auth') && authStore.isAuthenticated) {
      return await navigateTo('/')
    }
  })

  // Fournir les méthodes auth à l'application
  return {
    provide: {
      auth: {
        isAuthenticated: () => authStore.isAuthenticated,
        user: () => authStore.user,
        userRole: () => authStore.userRole
      }
    }
  }
})

import { defineNuxtRouteMiddleware, navigateTo } from '#app'

export default defineNuxtRouteMiddleware((to, from) => {
    // Vérifier si le token existe
    const token = localStorage.getItem('authToken')

    if (!token) {
        // Rediriger vers la page de connexion si pas de token
        return navigateTo('/login')
    }
}) 
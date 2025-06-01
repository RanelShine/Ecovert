import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.hook('app:created', () => {
        nuxtApp.vueApp.router?.beforeEach((to, from, next) => {
            // Vérifier si la route nécessite une authentification
            if (to.meta.auth) {
                const token = localStorage.getItem('authToken')
                if (!token) {
                    // Rediriger vers la page de connexion si pas de token
                    return next('/login')
                }
            }
            return next()
        })
    })
}) 
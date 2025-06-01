import { ref, computed } from 'vue'
import type { User } from '~/types'

const user = ref<User | null>(null)
const token = ref<string | null>(null)

export function useAuth() {
    const isAuthenticated = computed(() => !!token.value)
    const isCtd = computed(() => user.value?.role === 'CTD')

    const login = async (credentials: { email: string; password: string }) => {
        try {
            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            })

            if (!response.ok) {
                throw new Error('Échec de la connexion')
            }

            const data = await response.json()
            token.value = data.token
            user.value = data.user
            localStorage.setItem('authToken', data.token)

            return true
        } catch (error) {
            console.error('Erreur de connexion:', error)
            return false
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        localStorage.removeItem('authToken')
    }

    const checkAuth = async () => {
        const storedToken = localStorage.getItem('authToken')
        if (!storedToken) {
            return false
        }

        try {
            const response = await fetch('/api/auth/me/', {
                headers: {
                    'Authorization': `Bearer ${storedToken}`
                }
            })

            if (!response.ok) {
                throw new Error('Token invalide')
            }

            const data = await response.json()
            token.value = storedToken
            user.value = data
            return true
        } catch (error) {
            console.error('Erreur de vérification:', error)
            logout()
            return false
        }
    }

    return {
        user,
        token,
        isAuthenticated,
        isCtd,
        login,
        logout,
        checkAuth
    }
} 
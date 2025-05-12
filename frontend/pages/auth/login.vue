<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-gray-900">
            Connexion
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Ou
            <NuxtLink to="/auth/register" class="font-medium text-green-600 hover:text-green-500">
              créer un nouveau compte
            </NuxtLink>
          </p>
        </div>
        <form class="mt-2 bg-green-100 p-7 rounded-xl space-y-6" @submit.prevent="login">
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label for="email-address" class="sr-only">Adresse e-mail</label>
              <input id="email-address" name="email" type="email" autocomplete="email" required
                v-model="email"
                class="appearance-none mb-4 relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900  focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
                placeholder="Adresse e-mail"
              />
            </div>
            <div>
              <label for="password" class="sr-only">Mot de passe</label>
              <input id="password" name="password" type="password" autocomplete="current-password" required
                v-model="password"
                class="appearance-none mb-4 relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
                placeholder="Mot de passe"
              />
            </div>
          </div>
  
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input id="remember-me" name="remember-me" type="checkbox" 
                v-model="rememberMe"
                class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Se souvenir de moi
              </label>
            </div>
  
            <div class="text-sm">
              <a href="#" class="font-medium  hover:text-green-500">
                Mot de passe oublié?
              </a>
            </div>
          </div>
  
          <div>
            <button type="submit" 
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              :disabled="loading"
            >
              <span v-if="loading">Chargement...</span>
              <span v-else>Se connecter</span>
            </button>
          </div>
          
          <div v-if="error" class="text-red-600 text-center">
            {{ error }}
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'


const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const loading = ref(false)
const error = ref(null)

const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  loading.value = true
  error.value = null

  try {
    const result = await authStore.login({
  email: email.value,
  password: password.value
})

if (user.role === "Citoyens") {
  router.push('/dashboard')
} else {
  router.push('/')
}

  } catch (err) {
    if (err.response && err.response.data) {
      error.value = err.response.data.message || "Erreur de connexion"
    } else {
      error.value = "Une erreur s'est produite lors de la connexion"
    }
  } finally {
    loading.value = false
  }
}
</script>

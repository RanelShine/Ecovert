<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          Créer un compte
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Ou
          <NuxtLink to="/auth/login" class="font-medium text-green-600 hover:text-green-500">
            se connecter avec un compte existant
          </NuxtLink>
        </p>
      </div>
      <form class="mt-2 bg-green-100 p-7 rounded-xl space-y-6" @submit.prevent="register">
        <div class="rounded-md shadow-sm -space-y-px">
          <!-- Email -->
          <div class="relative">
            <input id="email-address" name="email" type="email" autocomplete="email" required
              v-model="email"
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
              placeholder="Adresse e-mail"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: mail -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M16 12H8m8 0l-4-4m4 4l-4 4"/>
              </svg>
            </div>
          </div>

          <!-- Nom -->
          <div class="relative">
            <input id="name" name="name" type="text" required
              v-model="name"
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
              placeholder="Nom"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: user -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M5.121 17.804A6 6 0 0112 15a6 6 0 016.879 2.804M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
          </div>

          <!-- Prénom -->
          <div class="relative">
            <input id="surname" name="surname" type="text" required
              v-model="surname"
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
              placeholder="Prénom"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: identification -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </div>
          </div>

          <!-- Téléphone -->
          <div class="relative">
            <input id="phone" name="phone" type="text" required
              v-model="phone"
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
              placeholder="Téléphone"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: phone -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 5a2 2 0 012-2h3.28a1 1 0 01.949.684l1.32 3.956a1 1 0 01-.217 1.01l-2.457 2.457a11.042 11.042 0 005.292 5.292l2.457-2.457a1 1 0 011.01-.217l3.956 1.32a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C8.268 21 3 15.732 3 9V5z"/>
              </svg>
            </div>
          </div>

          <!-- Rôle -->
          <div class="relative">
            <select id="role" name="role" v-model="role" required
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm">
              <option disabled value="">Sélectionnez un rôle</option>
              <option value="Admin">Admin</option>
              <option value="ONG">ONG</option>
              <option value="Entreprise">Entreprise</option>
              <option value="Citoyen">Citoyen</option>
            </select>
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: briefcase -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m2 4H7a2 2 0 01-2-2V7a2 2 0 012-2h3.5l1-1h2l1 1H17a2 2 0 012 2v7a2 2 0 01-2 2z"/>
              </svg>
            </div>
          </div>

          <!-- Mot de passe -->
          <div class="relative">
            <input id="password" name="password" type="password" required
              v-model="password"
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
              placeholder="Mot de passe"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: lock -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 11c.828 0 1.5.672 1.5 1.5S12.828 14 12 14s-1.5-.672-1.5-1.5S11.172 11 12 11zM5 11V9a7 7 0 0114 0v2m-2 0v7a2 2 0 01-2 2H9a2 2 0 01-2-2v-7h10z"/>
              </svg>
            </div>
          </div>

          <!-- Confirmation mot de passe -->
          <div class="relative">
            <input id="password-confirm" name="password-confirm" type="password" required
              v-model="passwordConfirm"
              class="appearance-none mb-4 relative block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
              placeholder="Confirmer le mot de passe"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <!-- Heroicon: check -->
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M5 13l4 4L19 7"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Bouton -->
        <div>
          <button type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            :disabled="loading"
          >
            <span v-if="loading">Chargement...</span>
            <span v-else>S'inscrire</span>
          </button>
        </div>

        <!-- Erreur -->
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
import { useNuxtApp } from '#app'

// Variables réactives
const email = ref('')
const name = ref('')
const surname = ref('')
const phone = ref('')
const role = ref('')
const password = ref('')
const passwordConfirm = ref('')
const loading = ref(false)
const error = ref(null)

const router = useRouter()
const { $axios } = useNuxtApp()

const register = async () => {
  error.value = ''
  
  if (password.value !== passwordConfirm.value) {
    error.value = 'Les mots de passe ne correspondent pas.'
    return
  }

  loading.value = true
  try {
    const response = await $axios.post('/api/register', {
      email: email.value,
      name: name.value,
      surname: surname.value,
      phone: phone.value,
      role: role.value,
      password: password.value,
    })

    if (response.data.success) {
      // Redirection après inscription
      router.push('/auth/login')
    } else {
      error.value = response.data.message || 'Une erreur est survenue.'
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Erreur lors de l’inscription.'
  } finally {
    loading.value = false
  }
}

</script>

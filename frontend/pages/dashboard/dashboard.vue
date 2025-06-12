<template>
  <div class="max-w-6xl mx-auto py-8 px-4 dark:gray-900">
    <!-- Debug info détaillé (à retirer en production) -->
    <!-- <div class="mb-4 p-4 bg-gray-100 rounded text-sm space-y-2">
      <div><strong>Debug Info:</strong></div>
      <div>Role détecté: <span class="font-mono bg-yellow-200 px-1">"{{ userRole }}"</span></div>
      <div>isHydrated: <span class="font-mono">{{ isHydrated }}</span></div>
      <div>userData brut: <span class="font-mono text-xs">{{ rawUserData }}</span></div>
      <div>authToken présent: <span class="font-mono">{{ !!authToken }}</span></div>
      <div v-if="debugInfo.length > 0">
        <strong>Logs de debug:</strong>
        <ul class="text-xs mt-1">
          <li v-for="(log, index) in debugInfo" :key="index" class="font-mono">{{ log }}</li>
        </ul>
      </div>
      <button 
        @click="refreshUserData" 
        class="bg-blue-500 text-white px-3 py-1 rounded text-xs hover:bg-blue-600 mr-2"
      >
        Actualiser les données utilisateur
      </button>
      <button 
        @click="clearAuthAndRedirect" 
        class="bg-red-500 text-white px-3 py-1 rounded text-xs hover:bg-red-600"
      >
        Forcer reconnexion
      </button>
    </div> -->
   
    <!-- Affichage conditionnel seulement après hydratation -->
    <div v-if="isHydrated">
      <!-- ONG ou entreprise -->
      <div v-if="userRole === 'ong' || userRole === 'entreprise'">
        <entreprisesection />
      </div>
     
      <!-- Citoyens -->
      <div v-else-if="userRole === 'citoyen'">
        <citoyensection />
      </div>
     
      <!-- CTD -->
      <div v-else-if="userRole === 'ctd'">
        <ctdsection />
      </div>
     
      <!-- Fallback si aucun rôle ne correspond -->
      <div v-else>
        <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
          <p class="text-red-600">⚠️ Rôle utilisateur non reconnu: <strong>{{ userRole }}</strong></p>
          <p class="text-sm text-red-500 mt-2">Affichage par défaut de la section citoyen.</p>
        </div>
        <citoyensection />
      </div>
    </div>
   
    <!-- Loading pendant l'hydratation -->
    <div v-else class="flex justify-center items-center py-12">
      <div class="text-gray-500 flex items-center space-x-2">
        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-500"></div>
        <span>Chargement des données utilisateur...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import entreprisesection from '~/components/sections/signalement/entreprise section.vue'
import citoyensection from '~/components/sections/signalement/citoyensection.vue'
import ctdsection from '~/components/sections/signalement/ctdsection.vue'

definePageMeta({
  layout: 'dashboard'
})

const userRole = ref<string>('')
const isHydrated = ref<boolean>(false)
const rawUserData = ref<string>('')
const authToken = ref<string>('')
const debugInfo = ref<string[]>([])

// Fonction pour ajouter des logs de debug
const addDebugLog = (message: string) => {
  debugInfo.value.push(`${new Date().toLocaleTimeString()}: ${message}`)
  console.log(`[DEBUG] ${message}`)
}

// Fonction pour tester différents formats d'authentification
const testAuthFormats = async (endpoint: string, token: string): Promise<any> => {
  const authFormats = [
    { name: 'Bearer', header: `Bearer ${token}` },
    { name: 'Token', header: `Token ${token}` },
    { name: 'JWT', header: `JWT ${token}` },
    { name: 'Direct', header: token }
  ]

  for (const format of authFormats) {
    try {
      addDebugLog(`Test format auth "${format.name}" sur ${endpoint}`)
      const response = await fetch(endpoint, {
        headers: {
          'Authorization': format.header,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const userData = await response.json()
        addDebugLog(`✅ Format auth fonctionnel: ${format.name}`)
        addDebugLog(`Données reçues: ${JSON.stringify(userData)}`)
        return { userData, authFormat: format.name }
      } else {
        addDebugLog(`❌ Format "${format.name}": ${response.status} ${response.statusText}`)
      }
    } catch (error) {
      addDebugLog(`❌ Format "${format.name}": Erreur - ${error}`)
    }
  }
  
  return null
}

// Fonction pour récupérer les données utilisateur depuis l'API
const fetchUserDataFromAPI = async (): Promise<any> => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) {
      addDebugLog('Pas de token trouvé')
      return null
    }

    addDebugLog(`Token: ${token.substring(0, 20)}...`)

    // Tester l'endpoint principal identifié
    const mainEndpoint = 'http://localhost:8000/api/accounts/me/'
    addDebugLog(`Test de l'endpoint principal: ${mainEndpoint}`)
    
    const result = await testAuthFormats(mainEndpoint, token)
    
    if (result) {
      addDebugLog(`✅ Authentification réussie avec format: ${result.authFormat}`)
      addDebugLog(`Role détecté: ${result.userData.role || 'non défini'}`)
      
      // Mettre à jour le localStorage avec les données fraîches
      localStorage.setItem('userData', JSON.stringify(result.userData))
      
      return result.userData
    }

    // Si l'endpoint principal ne fonctionne pas, tester d'autres endpoints
    const otherEndpoints = [
      'http://localhost:8000/api/auth/me/',
      'http://localhost:8000/api/users/me/',
      'http://localhost:8000/api/profile/'
    ]

    for (const endpoint of otherEndpoints) {
      addDebugLog(`Test endpoint alternatif: ${endpoint}`)
      const result = await testAuthFormats(endpoint, token)
      
      if (result) {
        addDebugLog(`✅ Endpoint alternatif fonctionnel: ${endpoint}`)
        localStorage.setItem('userData', JSON.stringify(result.userData))
        return result.userData
      }
    }

    addDebugLog('❌ Aucun endpoint/format d\'auth fonctionnel trouvé')
    
    // Vérifier si le token est expiré
    try {
      const tokenParts = token.split('.')
      if (tokenParts.length === 3) {
        const payload = JSON.parse(atob(tokenParts[1]))
        const exp = payload.exp * 1000
        const now = Date.now()
        
        if (exp < now) {
          addDebugLog('🕒 Token expiré - reconnexion nécessaire')
        } else {
          addDebugLog(`🕒 Token valide jusqu'à: ${new Date(exp).toLocaleString()}`)
        }
      }
    } catch (tokenError) {
      addDebugLog('❌ Token invalide ou mal formaté')
    }

    return null
  } catch (error) {
    addDebugLog(`Erreur lors de la récupération API: ${error}`)
    return null
  }
}

// Fonction pour récupérer le rôle utilisateur
const getUserRole = async (): Promise<string> => {
  try {
    addDebugLog('Début de getUserRole')
    
    // Vérifier si on est côté client
    if (typeof window === 'undefined') {
      addDebugLog('Côté serveur - pas de localStorage disponible')
      return 'citoyen'
    }

    // Récupérer le token
    const token = localStorage.getItem('authToken')
    authToken.value = token || ''
    addDebugLog(`Token présent: ${!!token}`)

    // Essayer d'abord les données du localStorage
    const localUserData = localStorage.getItem('userData')
    rawUserData.value = localUserData || 'null'
    addDebugLog(`userData localStorage: ${localUserData}`)

    let userData = null
    
    if (localUserData) {
      try {
        userData = JSON.parse(localUserData)
        addDebugLog(`userData parsé: ${JSON.stringify(userData)}`)
        addDebugLog(`Role depuis localStorage: ${userData.role}`)
      } catch (parseError) {
        addDebugLog(`Erreur parsing localStorage: ${parseError}`)
      }
    }

    // Si pas de données locales valides, récupérer depuis l'API
    if (!userData || !userData.role) {
      addDebugLog('Récupération depuis l\'API nécessaire')
      userData = await fetchUserDataFromAPI()
    }

    if (userData && userData.role) {
      const role = userData.role.toLowerCase().trim()
      addDebugLog(`Role final déterminé: "${role}"`)
      
      // Vérifier que le rôle est valide
      const validRoles = ['citoyen', 'ctd', 'ong', 'entreprise']
      if (!validRoles.includes(role)) {
        addDebugLog(`Role invalide "${role}", utilisation de "citoyen" par défaut`)
        return 'citoyen'
      }
      
      return role
    }

    addDebugLog('Aucune donnée utilisateur valide trouvée - retour citoyen par défaut')
    return 'citoyen'
    
  } catch (error) {
    addDebugLog(`Erreur dans getUserRole: ${error}`)
    return 'citoyen'
  }
}

// Fonction pour actualiser les données utilisateur
const refreshUserData = async () => {
  addDebugLog('Actualisation manuelle des données utilisateur')
  userRole.value = await getUserRole()
}

// Fonction pour forcer une reconnexion
const clearAuthAndRedirect = () => {
  addDebugLog('Nettoyage des données d\'authentification')
  localStorage.removeItem('authToken')
  localStorage.removeItem('userData')
  
  // Rediriger vers la page de connexion
  // Adaptez selon votre router
  window.location.href = '/login' // ou navigateTo('/login') si vous utilisez Nuxt
}

onMounted(async () => {
  addDebugLog('Composant monté - début de l\'initialisation')
  
  // Attendre la prochaine tick pour s'assurer que le DOM est prêt
  await nextTick()
  addDebugLog('NextTick terminé')

  userRole.value = await getUserRole()
  isHydrated.value = true

  addDebugLog(`Initialisation terminée - Role final: "${userRole.value}"`)
})
</script>

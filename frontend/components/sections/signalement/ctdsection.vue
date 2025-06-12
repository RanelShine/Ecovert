<!-- section ctdsection -->
<template>
  <div class="flex justify-between mb-6 items-center">
      <h1 class="text-3xl font-bold text-green-700 dark:text-green-600">Gestion des Signalements</h1>
  </div>
  <!-- Filtres -->
  <div class="bg-white rounded-lg shadow p-3 sm:p-4 mb-4 sm:mb-6 dark:bg-gray-600 dark:text-gray-200">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 gap-3 sm:gap-0">
      <h3 class="text-lg font-semibold">Filtres</h3>
      <!-- Nouveau bouton pour la carte -->
      <button @click="navigateToMap"
        class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center justify-center gap-2 text-sm sm:text-base w-full sm:w-auto">
        <Icon name="mdi:map" class="text-xl" />
        <span class="hidden xs:inline">Voir sur la carte</span>
        <span class="xs:hidden">Carte</span>
      </button>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 ">
      <select v-model="filtreStatut" @change="chargerTousSignalements" 
        class="border rounded p-2 text-sm sm:text-base w-full">
        <option value="">Tous les statuts</option>
        <option v-for="statut in statutChoices" :key="statut.value" :value="statut.value">
          {{ statut.label }}
        </option>
      </select>
      <select v-model="filtreType" @change="chargerTousSignalements" 
        class="border rounded p-2 text-sm sm:text-base w-full">
        <option value="">Tous les types</option>
        <option v-for="type in typeChoices" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
      <button @click="resetFiltres" 
        class="bg-gray-500 text-white px-4 py-2 rounded dark:hover:bg-gray-700 dark:bg-gray-900 hover:bg-gray-600 text-sm sm:text-base sm:col-span-2 lg:col-span-1">
        Réinitialiser
      </button>
    </div>
  </div>

  <!-- Tous les signalements -->
  <div class="bg-white rounded-lg shadow overflow-hidden dark:bg-gray-400  ">
    <div class="bg-green-600 text-white p-3 sm:p-4 font-semibold flex flex-col xs:flex-row xs:justify-between xs:items-center gap-2 xs:gap-0 dark:bg-green-600">
      <span class="text-sm sm:text-base">Tous les signalements ({{ tousSignalements.length }})</span>
      <button @click="chargerTousSignalements" 
        class="bg-green-700 px-3 py-1 rounded text-xs sm:text-sm hover:bg-green-800 w-full xs:w-auto">
        Actualiser
      </button>
    </div>
    
    <!-- Version desktop/tablette (masquée sur mobile) -->
    <div class="hidden md:block p-4 bg-gray-50 overflow-x-auto dark:bg-gray-600">
      <table class="w-full text-left border border-collapse min-w-full">
        <thead class="bg-green-100 dark:bg-green-600">
          <tr>
            <th class="p-2 border text-sm lg:text-base">Objet</th>
            <th class="p-2 border text-sm lg:text-base">Type</th>
            <th class="p-2 border text-sm lg:text-base">Date</th>
            <th class="p-2 border text-sm lg:text-base">Statut</th>
            <th class="p-2 border text-sm lg:text-base">Changer statut</th>
            <th class="p-2 border text-sm lg:text-base">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in tousSignalements" :key="s.id" class="bg-white dark:bg-gray-800 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600">
            <td class="p-2 border text-sm lg:text-base">
              <div class="max-w-xs truncate " :title="s.objet">{{ s.objet }}</div>
            </td>
            <td class="p-2 border capitalize text-sm lg:text-base">{{ s.type_signalement_display }}</td>
            <td class="p-2 border text-sm lg:text-base whitespace-nowrap">{{ formatDate(s.date_signalement) }}</td>
            <td class="p-2 border">
              <span :class="statusClass(s.statut)" class="text-xs lg:text-sm">
                {{ s.statut_display }}
              </span>
            </td>
            <td class="p-2 border">
              <select :value="s.statut" @change="(event) => {
                const target = event.target as HTMLSelectElement;
                if (target && target.value) {
                  changerStatut(s.id, target.value);
                }
              }" class="border p-1 rounded text-xs lg:text-sm w-full">
                <option v-for="statut in statutChoices" :key="statut.value" :value="statut.value">
                  {{ statut.label }}
                </option>
              </select>
            </td>
            <td class="p-2 border">
              <button @click="voirDetails(s)"
                class="bg-blue-500 text-white px-2 py-1 rounded text-xs hover:bg-blue-600 w-full">
                Détails
              </button>
            </td>
          </tr>
          <tr v-if="tousSignalements.length === 0">
            <td colspan="6" class="p-4 text-center text-gray-500 text-sm lg:text-base">Aucun signalement trouvé.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Version mobile (masquée sur desktop/tablette) -->
    <div class="md:hidden">
      <div v-for="s in tousSignalements" :key="s.id" 
        class="border-b border-gray-200 p-4 hover:bg-gray-50">
        
        <!-- En-tête de la card mobile -->
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="font-semibold text-sm text-gray-900 truncate mb-1" :title="s.objet">
              {{ s.objet }}
            </h4>
            <div class="flex flex-wrap gap-2 text-xs">
              <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                {{ s.type_signalement_display }}
              </span>
              <span :class="statusClass(s.statut) + ' px-2 py-1 rounded-full bg-gray-100'">
                {{ s.statut_display }}
              </span>
            </div>
          </div>
          <button @click="voirDetails(s)"
            class="bg-blue-500 text-white px-3 py-1 rounded text-xs hover:bg-blue-600 ml-2 flex-shrink-0">
            Détails
          </button>
        </div>

        <!-- Informations supplémentaires -->
        <div class="text-xs text-gray-600 mb-3">
          <div>{{ formatDateMobile(s.date_signalement) }}</div>
        </div>

        <!-- Changer statut sur mobile -->
        <div class="flex items-center gap-2">
          <label class="text-xs font-medium text-gray-700 flex-shrink-0">Statut:</label>
          <select :value="s.statut" @change="(event) => {
            const target = event.target as HTMLSelectElement;
            if (target && target.value) {
              changerStatut(s.id, target.value);
            }
          }" class="border rounded p-1 text-xs flex-1">
            <option v-for="statut in statutChoices" :key="statut.value" :value="statut.value">
              {{ statut.label }}
            </option>
          </select>
        </div>
      </div>
      
      <div v-if="tousSignalements.length === 0" class="p-8 text-center text-gray-500 text-sm">
        Aucun signalement trouvé.
      </div>
    </div>
  </div>

  <!-- Modal Détails - Responsive -->
  <div v-if="showDetails && selectedSignalement"
    class="fixed inset-0 bg-black  bg-opacity-75 flex items-center justify-center z-50 p-2 sm:p-4">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 sm:p-6 w-full max-w-2xl max-h-[95vh] sm:max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-start mb-4">
        <h3 class="text-lg sm:text-xl font-semibold dark:text-white pr-4">Détails du signalement</h3>
        <button @click="showDetails = false" 
          class="text-gray-500 hover:text-gray-700 text-xl sm:text-2xl flex-shrink-0">✕</button>
      </div>

      <div class="space-y-3 sm:space-y-4 text-sm sm:text-base">
        <div class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Objet :</strong> 
          <span class="break-words">{{ selectedSignalement.objet }}</span>
        </div>
        <div class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Type :</strong> 
          <span class="capitalize">{{ selectedSignalement.type_signalement_display }}</span>
        </div>
        <div class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Description :</strong> 
          <span class="break-words">{{ selectedSignalement.description }}</span>
        </div>
        <div class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Localisation :</strong> 
          <span class="break-words">{{ selectedSignalement.localisation }}</span>
        </div>
        <div class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Statut :</strong>
          <span :class="statusClass(selectedSignalement.statut) + ' px-2 py-1 rounded bg-gray-100'">
            {{ selectedSignalement.statut_display }}
          </span>
        </div>
        <div class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Date de signalement :</strong> 
          <span>{{ formatDate(selectedSignalement.date_signalement) }}</span>
        </div>
        <div v-if="selectedSignalement.date_resolution" class="border-b pb-2">
          <strong class="block text-gray-700 dark:text-green-600 mb-1">Date de résolution :</strong> 
          <span>{{ formatDate(selectedSignalement.date_resolution) }}</span>
        </div>
      </div>
      
      <!-- Bouton de fermeture en bas sur mobile -->
      <div class="mt-6 sm:hidden">
        <button @click="showDetails = false" 
          class="w-full bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600">
          Fermer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Signalement {
  id: number
  objet: string
  description: string
  type_signalement: string
  type_signalement_display: string
  date_signalement: string
  date_resolution?: string
  statut: string
  statut_display: string
  localisation: string
  utilisateur_nom: string
  photo_id?: number
}

interface Choice {
  value: string
  label: string
}

// Données
const token = localStorage.getItem('authToken')
const tousSignalements = ref<Signalement[]>([])
const typeChoices = ref<Choice[]>([
  { value: 'pollution', label: 'Pollution' },
  { value: 'dechets', label: 'Déchets' },
  { value: 'climat', label: 'Climat' }
])
const statutChoices = ref<Choice[]>([
  { value: 'en_attente', label: 'En attente' },
  { value: 'en_cours', label: 'En cours' },
  { value: 'traite', label: 'Traité' }
])

// Filtres
const filtreStatut = ref('')
const filtreType = ref('')

// Modal détails
const showDetails = ref(false)
const selectedSignalement = ref<Signalement | null>(null)

const router = useRouter()

// Charger les choix disponibles
const chargerChoix = async () => {
  console.log('🎛️ Début chargerChoix - Token:', token ? 'présent' : 'absent')

  try {
    const response = await fetch('http://localhost:8000/api/signalements/choices/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    console.log('📊 Réponse choix - Status:', response.status, 'OK:', response.ok)

    if (response.ok) {
      const data = await response.json()
      console.log('📦 Choix reçus:', data)

      if (data.types_signalement) {
        typeChoices.value = data.types_signalement
        console.log('✅ Types chargés:', data.types_signalement.length)
      }
      if (data.statuts) {
        statutChoices.value = data.statuts
        console.log('✅ Statuts chargés:', data.statuts.length)
      }
    } else {
      const errorText = await response.text()
      console.error('❌ Erreur HTTP choix:', response.status, response.statusText, 'Body:', errorText)
    }
  } catch (error) {
    console.error('💥 Erreur lors du chargement des choix:', error)
  }
}

// Charger tous les signalements (pour CTD)
const chargerTousSignalements = async () => {
  console.log('🔍 Début chargerTousSignalements - Token:', token ? 'présent' : 'absent')

  try {
    let url = 'http://localhost:8000/api/signalements/liste/'
    const params = new URLSearchParams()

    if (filtreStatut.value) params.append('statut', filtreStatut.value)
    if (filtreType.value) params.append('type', filtreType.value)

    if (params.toString()) {
      url += '?' + params.toString()
    }

    console.log('📡 URL appelée:', url)

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    console.log('📊 Réponse API - Status:', response.status, 'OK:', response.ok)

    if (response.ok) {
      const data = await response.json()
      console.log('📦 Données reçues:', data)
      console.log('📋 Structure data:', Object.keys(data))

      // Essayer différentes structures possibles
      if (data.signalements) {
        tousSignalements.value = data.signalements
        console.log('✅ Signalements chargés depuis data.signalements:', data.signalements.length)
      } else if (Array.isArray(data)) {
        tousSignalements.value = data
        console.log('✅ Signalements chargés depuis data (array):', data.length)
      } else if (data.results) {
        tousSignalements.value = data.results
        console.log('✅ Signalements chargés depuis data.results:', data.results.length)
      } else {
        console.log('⚠️ Structure de données non reconnue:', data)
        tousSignalements.value = []
      }
    } else {
      const errorText = await response.text()
      console.error('❌ Erreur HTTP:', response.status, response.statusText, 'Body:', errorText)
    }
  } catch (error) {
    console.error('💥 Erreur lors du chargement des signalements:', error)
  }

  console.log('🏁 Fin chargerTousSignalements - Nombre de signalements:', tousSignalements.value.length)
}

// Réinitialiser les filtres
const resetFiltres = () => {
  filtreStatut.value = ''
  filtreType.value = ''
  chargerTousSignalements()
}

// Changer le statut (CTD uniquement)
const changerStatut = async (signalementId: number, nouveauStatut: string) => {
  try {
    const response = await fetch(`http://localhost:8000/api/signalements/update-statut/${signalementId}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ statut: nouveauStatut })
    })

    if (response.ok) {
      alert('Statut modifié avec succès !')
      await chargerTousSignalements()
    } else {
      throw new Error('Erreur lors de la modification du statut')
    }
  } catch (error) {
    alert('Erreur: ' + error)
  }
}

// Voir les détails
const voirDetails = async (signalement: Signalement) => {
  try {
    const response = await fetch(`http://localhost:8000/api/signalements/detail/${signalement.id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    if (response.ok) {
      const data = await response.json()
      selectedSignalement.value = data
      showDetails.value = true
    } else {
      console.error('Erreur HTTP:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('Erreur lors du chargement des détails:', error)
  }
}

// Utilitaires
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Format de date plus compact pour mobile
const formatDateMobile = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const statusClass = (status: string) => {
  switch (status) {
    case 'en_cours': return 'text-yellow-600 font-semibold'
    case 'traite': return 'text-green-600 font-semibold'
    case 'en_attente': return 'text-gray-600 font-semibold'
    default: return 'text-gray-600'
  }
}

// Fonction de navigation vers la carte
const navigateToMap = () => {
  router.push('/dashboard/map')
}

// Initialisation
onMounted(async () => {
  console.log('🚀 Composant CTD monté - Initialisation')
  console.log('🔑 Token présent:', !!token)
  console.log('🔑 Token value:', token ? token.substring(0, 20) + '...' : 'null')

  if (!token) {
    console.warn('🔐 Aucun token trouvé. Redirection possible...')
    router.push('/auth/login') 
  } else {
    chargerTousSignalements()
    chargerChoix()
  }

  console.log('✅ Initialisation terminée')
})
</script>

<style scoped>
/* Ajout de classes personnalisées pour extra small screens */
@media (min-width: 475px) {
  .xs\:inline { display: inline; }
  .xs\:hidden { display: none; }
  .xs\:flex-row { flex-direction: row; }
  .xs\:justify-between { justify-content: space-between; }
  .xs\:items-center { align-items: center; }
  .xs\:w-auto { width: auto; }
}

@media (max-width: 474px) {
  .xs\:inline { display: none; }
  .xs\:hidden { display: inline; }
}

/* Amélioration de l'affichage des longues chaînes */
.break-words {
  word-wrap: break-word;
  word-break: break-word;
  hyphens: auto;
}

/* Styles pour les sélecteurs sur mobile */
@media (max-width: 768px) {
  select {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 0.5rem center;
    background-repeat: no-repeat;
    background-size: 1.5em 1.5em;
    padding-right: 2.5rem;
  }
}
</style>
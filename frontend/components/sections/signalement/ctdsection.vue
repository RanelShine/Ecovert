<!-- section ctdsection -->
<template>
  <!-- Filtres -->
  <div class="bg-white rounded-lg shadow p-4 mb-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">Filtres</h3>
      <!-- Nouveau bouton pour la carte -->
      <button @click="navigateToMap"
        class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2">
        <Icon name="mdi:map" class="text-xl" />
        Voir sur la carte
      </button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <select v-model="filtreStatut" @change="chargerTousSignalements" class="border rounded p-2">
        <option value="">Tous les statuts</option>
        <option v-for="statut in statutChoices" :key="statut.value" :value="statut.value">
          {{ statut.label }}
        </option>
      </select>
      <select v-model="filtreType" @change="chargerTousSignalements" class="border rounded p-2">
        <option value="">Tous les types</option>
        <option v-for="type in typeChoices" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
      <button @click="resetFiltres" class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
        Réinitialiser
      </button>
    </div>
  </div>

  <!-- Tous les signalements -->
  <div class="bg-white rounded-lg shadow">
    <div class="bg-green-600 text-white p-4 font-semibold rounded-t-lg flex justify-between items-center">
      <span>Tous les signalements ({{ tousSignalements.length }})</span>
      <button @click="chargerTousSignalements" class="bg-green-700 px-3 py-1 rounded text-sm hover:bg-green-800">
        Actualiser
      </button>
    </div>
    <div class="p-4 bg-gray-50 overflow-x-auto">
      <table class="w-full text-left border border-collapse">
        <thead class="bg-green-100">
          <tr>
            <th class="p-2 border">Objet</th>
            <th class="p-2 border">Type</th>
            <!-- <th class="p-2 border">Utilisateur</th> -->
            <th class="p-2 border">Date</th>
            <th class="p-2 border">Statut</th>
            <th class="p-2 border">Changer statut</th>
            <th class="p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in tousSignalements" :key="s.id" class="bg-white hover:bg-gray-50">
            <td class="p-2 border">{{ s.objet }}</td>
            <td class="p-2 border capitalize">{{ s.type_signalement_display }}</td>
            <!-- <td class="p-2 border">{{ s.utilisateur_nom }}</td> -->
            <td class="p-2 border">{{ formatDate(s.date_signalement) }}</td>
            <td class="p-2 border">
              <span :class="statusClass(s.statut)">
                {{ s.statut_display }}
              </span>
            </td>
            <td class="p-2 border">
              <select :value="s.statut" @change="(event) => {
                const target = event.target as HTMLSelectElement;
                if (target && target.value) {
                  changerStatut(s.id, target.value);
                }
              }" class="border p-1 rounded text-sm">
                <option v-for="statut in statutChoices" :key="statut.value" :value="statut.value">
                  {{ statut.label }}
                </option>
              </select>
            </td>
            <td class="p-2 border">
              <button @click="voirDetails(s)"
                class="bg-blue-500 text-white px-2 py-1 rounded text-xs mr-1 hover:bg-blue-600">
                Détails
              </button>
              <button @click="supprimerSignalement(s.id)"
                class="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600">
                Supprimer
              </button>
            </td>
          </tr>
          <tr v-if="tousSignalements.length === 0">
            <td colspan="7" class="p-4 text-center text-gray-500">Aucun signalement trouvé.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Modal Détails -->
  <div v-if="showDetails && selectedSignalement"
    class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-start mb-4">
        <h3 class="text-xl font-semibold">Détails du signalement</h3>
        <button @click="showDetails = false" class="text-gray-500 hover:text-gray-700">✕</button>
      </div>

      <div class="space-y-3">
        <div><strong>Objet :</strong> {{ selectedSignalement.objet }}</div>
        <div><strong>Type :</strong> {{ selectedSignalement.type_signalement_display }}</div>
        <div><strong>Description :</strong> {{ selectedSignalement.description }}</div>
        <div><strong>Localisation :</strong> {{ selectedSignalement.localisation }}</div>
        <div><strong>Statut :</strong>
          <span :class="statusClass(selectedSignalement.statut)">
            {{ selectedSignalement.statut_display }}
          </span>
        </div>
        <div><strong>Date de signalement :</strong> {{ formatDate(selectedSignalement.date_signalement) }}</div>
        <div v-if="selectedSignalement.date_resolution">
          <strong>Date de résolution :</strong> {{ formatDate(selectedSignalement.date_resolution) }}
        </div>
        <div><strong>Utilisateur :</strong> {{ selectedSignalement.utilisateur_nom }}</div>
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

// Supprimer un signalement
const supprimerSignalement = async (signalementId: number) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce signalement ?')) {
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/signalements/delete/${signalementId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      alert('Signalement supprimé avec succès !')
      await chargerTousSignalements()
    } else {
      throw new Error('Erreur lors de la suppression')
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

  await chargerChoix()
  await chargerTousSignalements()

  console.log('✅ Initialisation terminée')
})
</script>

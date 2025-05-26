<template>
  <div class="space-y-6">
    <!-- Header avec bouton d'ajout -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Gestion des Projets</h1>
      <button
        @click="showAddModal = true"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
      >
        + Nouveau Projet
      </button>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-sm font-medium text-gray-500">Total Projets</h3>
        <p class="text-3xl font-bold text-blue-600">{{ stats.total }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-sm font-medium text-gray-500">En Cours</h3>
        <p class="text-3xl font-bold text-yellow-600">{{ stats.enCours }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-sm font-medium text-gray-500">Terminés</h3>
        <p class="text-3xl font-bold text-green-600">{{ stats.termines }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-sm font-medium text-gray-500">Budget Total</h3>
        <p class="text-3xl font-bold text-purple-600">{{ formatCurrency(stats.budgetTotal) }}</p>
      </div>
    </div>

    <!-- Liste des projets -->
    <div class="bg-white rounded-lg shadow-md">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">Mes Projets</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Chargement des projets...</p>
        </div>
        
        <div v-else-if="projets.length === 0" class="text-center py-8">
          <p class="text-gray-500">Aucun projet trouvé</p>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="projet in projets"
            :key="projet.id"
            class="border rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer"
            @click="selectProjet(projet)"
          >
            <div v-if="projet.image" class="mb-4">
              <img
                :src="projet.image"
                :alt="projet.nom"
                class="w-full h-48 object-cover rounded-lg"
              />
            </div>
            <div class="space-y-2">
              <h3 class="font-semibold text-lg">{{ projet.nom }}</h3>
              <p class="text-gray-600 text-sm line-clamp-2">{{ projet.description }}</p>
              <div class="flex justify-between items-center">
                <span
                  :class="{
                    'bg-green-100 text-green-800': projet.statut === 'termine',
                    'bg-yellow-100 text-yellow-800': projet.statut === 'en_cours',
                    'bg-blue-100 text-blue-800': projet.statut === 'planifie',
                    'bg-red-100 text-red-800': projet.statut === 'suspendu'
                  }"
                  class="px-2 py-1 rounded-full text-xs font-medium"
                >
                  {{ getStatutLabel(projet.statut) }}
                </span>
                <span class="text-sm text-gray-500">{{ formatDate(projet.dateCreation) }}</span>
              </div>
              <div class="mt-2">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${projet.avancement}%` }"
                  ></div>
                </div>
                <p class="text-xs text-gray-500 mt-1">{{ projet.avancement }}% terminé</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal d'ajout de projet -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">{{ selectedProjet ? 'Modifier le Projet' : 'Nouveau Projet' }}</h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitProjet" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nom du projet</label>
            <input
              v-model="form.nom"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Nom du projet"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              v-model="form.description"
              required
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Description du projet"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Budget</label>
              <input
                v-model="form.budget"
                type="number"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Budget en FCFA"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Statut</label>
              <select
                v-model="form.statut"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="planifie">Planifié</option>
                <option value="en_cours">En cours</option>
                <option value="termine">Terminé</option>
                <option value="suspendu">Suspendu</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Date de début</label>
              <input
                v-model="form.dateDebut"
                type="date"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Date de fin prévue</label>
              <input
                v-model="form.dateFin"
                type="date"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Avancement (%)</label>
            <input
              v-model="form.avancement"
              type="number"
              min="0"
              max="100"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Pourcentage d'avancement"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Image du projet</label>
            <input
              @change="handleImageUpload"
              type="file"
              accept="image/*"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Document du projet</label>
            <input
              @change="handleFileUpload"
              type="file"
              accept=".pdf,.doc,.docx,.xls,.xlsx"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {{ submitting ? 'Enregistrement...' : (selectedProjet ? 'Modifier' : 'Créer') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'

// Types
interface Projet {
  id: number
  nom: string
  description: string
  budget: number
  statut: 'planifie' | 'en_cours' | 'termine' | 'suspendu'
  dateDebut: string
  dateFin: string
  avancement: number
  image?: string
  document?: string
  dateCreation: string
}

interface Stats {
  total: number
  enCours: number
  termines: number
  budgetTotal: number
}

// État réactif
const projets = ref<Projet[]>([])
const stats = ref<Stats>({
  total: 0,
  enCours: 0,
  termines: 0,
  budgetTotal: 0
})
const loading = ref(false)
const showAddModal = ref(false)
const selectedProjet = ref<Projet | null>(null)
const submitting = ref(false)

// Formulaire
const form = reactive({
  nom: '',
  description: '',
  budget: 0,
  statut: 'planifie' as Projet['statut'],
  dateDebut: '',
  dateFin: '',
  avancement: 0,
  image: null as File | null,
  document: null as File | null
})

// Configuration de l'API
const config = useRuntimeConfig()
const baseURL = config.public.apiBase || 'http://localhost:8000/api'

// Fonctions utilitaires
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'XOF',
    minimumFractionDigits: 0
  }).format(amount)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('fr-FR')
}

const getStatutLabel = (statut: 'planifie' | 'en_cours' | 'termine' | 'suspendu' | string) => {
  const labels: Record<'planifie' | 'en_cours' | 'termine' | 'suspendu', string> = {
    planifie: 'Planifié',
    en_cours: 'En cours',
    termine: 'Terminé',
    suspendu: 'Suspendu'
  }
  return (labels as Record<string, string>)[statut] || statut
}

// Gestion des fichiers
const handleImageUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    form.image = file
  }
}

const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    form.document = file
  }
}

// API calls
const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken')
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}

const fetchProjets = async () => {
  loading.value = true
  try {
    const response = await fetch(`${baseURL}/projets/`, {
      headers: getAuthHeaders()
    })
    if (response.ok) {
      const data = await response.json()
      projets.value = data.results || data
      calculateStats()
    }
  } catch (error) {
    console.error('Erreur lors du chargement des projets:', error)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.value = {
    total: projets.value.length,
    enCours: projets.value.filter(p => p.statut === 'en_cours').length,
    termines: projets.value.filter(p => p.statut === 'termine').length,
    budgetTotal: projets.value.reduce((sum, p) => sum + p.budget, 0)
  }
}

const submitProjet = async () => {
  submitting.value = true
  try {
    const formData = new FormData()
    
    // Ajouter les données du formulaire
    (Object.keys(form) as Array<keyof typeof form>).forEach((key: keyof typeof form) => {
      if (key !== 'image' && key !== 'document') {
        formData.append(key, String(form[key]))
      }
    })
    
    // Ajouter les fichiers
    if (form.image) {
      formData.append('image', form.image)
    }
    if (form.document) {
      formData.append('document', form.document)
    }

    const url = selectedProjet.value 
      ? `${baseURL}/projets/${selectedProjet.value.id}/`
      : `${baseURL}/projets/`
    
    const method = selectedProjet.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      },
      body: formData
    })

    if (response.ok) {
      await fetchProjets()
      closeModal()
    } else {
      throw new Error('Erreur lors de l\'enregistrement')
    }
  } catch (error) {
    console.error('Erreur:', error)
    alert('Erreur lors de l\'enregistrement du projet')
  } finally {
    submitting.value = false
  }
}

const selectProjet = (projet: Projet) => {
  selectedProjet.value = projet
  // Remplir le formulaire avec les données du projet
  (Object.keys(form) as Array<keyof Projet>).forEach((key) => {
    if (key !== 'image' && key !== 'document' && projet[key] !== undefined) {
      // @ts-expect-error: form may have extra keys not in Projet
      form[key] = projet[key]
    }
  })
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedProjet.value = null
  // Réinitialiser le formulaire
  Object.keys(form).forEach(key => {
    if (typeof form[key] === 'string') {
      form[key] = ''
    } else if (typeof form[key] === 'number') {
      form[key] = 0
    } else {
      form[key] = null
    }
  })
  form.statut = 'planifie'
}

// Lifecycle
onMounted(() => {
  fetchProjets()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
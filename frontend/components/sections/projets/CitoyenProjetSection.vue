<template>
    <div class="space-y-6">
        <!-- En-tête -->
        <div class="mb-6">
            <h1 class="text-2xl font-bold text-gray-900">Demande de comptes sur les projets</h1>
            <p class="mt-2 text-sm text-gray-600">Sélectionnez un projet et posez vos questions à la commune</p>
        </div>

        <!-- Formulaire de demande -->
        <div class="bg-white rounded-lg shadow p-6">
            <form @submit.prevent="submitDemande" class="space-y-4">
                <!-- Sélection du projet -->
                <div>
                    <label for="projet" class="block text-sm font-medium text-gray-700 mb-1">Projet concerné</label>
                    <select id="projet" v-model="form.projetId" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="">Sélectionnez un projet</option>
                        <option v-for="projet in projets" :key="projet.id" :value="projet.id">
                            {{ projet.nom }}
                        </option>
                    </select>
                </div>

                <!-- Question/Demande -->
                <div>
                    <label for="question" class="block text-sm font-medium text-gray-700 mb-1">Votre question ou
                        demande</label>
                    <textarea id="question" v-model="form.question" rows="4" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="Décrivez votre demande de comptes concernant ce projet..."></textarea>
                </div>

                <!-- Bouton de soumission -->
                <div class="flex justify-end">
                    <button type="submit" :disabled="loading"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
                        <span v-if="loading" class="mr-2">
                            <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                </path>
                            </svg>
                        </span>
                        {{ loading ? 'Envoi en cours...' : 'Envoyer la demande' }}
                    </button>
                </div>
            </form>
        </div>

        <!-- Liste des projets -->
        <div class="bg-white rounded-lg shadow">
            <div class="p-6 border-b">
                <h2 class="text-lg font-semibold text-gray-900">Projets de la commune</h2>
            </div>
            <div class="p-6">
                <div v-if="loading" class="text-center py-8">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p class="mt-4 text-gray-600">Chargement des projets...</p>
                </div>

                <div v-else-if="projets.length === 0" class="text-center py-8">
                    <p class="text-gray-500">Aucun projet disponible pour le moment</p>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="projet in projets" :key="projet.id" class="border rounded-lg p-4">
                        <h3 class="font-semibold text-lg mb-2">{{ projet.nom }}</h3>
                        <p class="text-gray-600 text-sm mb-4">{{ projet.description }}</p>
                        <button @click="selectProjet(projet)"
                            class="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
                            Demander des comptes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const API_BASE_URL = 'http://localhost:8000'

interface Projet {
    id: number
    nom: string
    description: string
    statut: string
}

const projets = ref<Projet[]>([])
const loading = ref(false)
const form = ref({
    projetId: '',
    question: ''
})

// Charger les projets
const fetchProjets = async () => {
    loading.value = true
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) throw new Error('Erreur lors du chargement des projets')

        const data = await response.json()
        projets.value = data.results || data
    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Erreur lors du chargement des projets')
    } finally {
        loading.value = false
    }
}

// Sélectionner un projet pour la demande
const selectProjet = (projet: Projet) => {
    form.value.projetId = projet.id
    // Faire défiler jusqu'au formulaire
    document.querySelector('#projet')?.scrollIntoView({ behavior: 'smooth' })
}

// Soumettre la demande
const submitDemande = async () => {
    loading.value = true
    try {
        const response = await fetch(`${API_BASE_URL}/api/projects/accountability/create/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                project: form.value.projetId,
                question: form.value.question
            })
        })

        if (!response.ok) throw new Error('Erreur lors de l\'envoi de la demande')

        toast.success('Votre demande a été envoyée avec succès')
        // Réinitialiser le formulaire
        form.value = {
            projetId: '',
            question: ''
        }
    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Erreur lors de l\'envoi de la demande')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchProjets()
})
</script>
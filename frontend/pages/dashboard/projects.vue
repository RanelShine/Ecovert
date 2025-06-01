<template>
    <div class="min-h-screen bg-gray-100">

        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <!-- En-tête -->
            <div class="mb-6 flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900">
                        Projets de la commune
                    </h1>
                    <p class="mt-2 text-sm text-gray-600">
                        Consultez les projets en cours et participez à la redevabilité
                    </p>
                </div>

                <!-- Bouton d'ajout pour les CTD -->
                <button v-if="user?.role === 'CTD'" @click="showProjectForm = true"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    <Icon name="mdi:plus" class="mr-2" />
                    Nouveau projet
                </button>
            </div>

            <!-- Filtres -->
            <div class="bg-white p-4 rounded-lg shadow mb-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Recherche -->
                    <div class="relative">
                        <input type="text" v-model="searchQuery" placeholder="Rechercher un projet..."
                            class="w-full pl-10 pr-4 py-2 border rounded-lg">
                        <Icon name="mdi:magnify"
                            class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    </div>

                    <!-- Filtre par statut -->
                    <select v-model="statusFilter" class="w-full py-2 px-4 border rounded-lg">
                        <option value="">Tous les statuts</option>
                        <option v-for="status in projectStatuses" :key="status" :value="status">
                            {{ getStatusLabel(status) }}
                        </option>
                    </select>

                    <!-- Tri -->
                    <select v-model="sortBy" class="w-full py-2 px-4 border rounded-lg">
                        <option value="created_at">Plus récents</option>
                        <option value="-created_at">Plus anciens</option>
                        <option value="title">Ordre alphabétique</option>
                        <option value="-accountability_count">Plus de demandes</option>
                    </select>
                </div>
            </div>

            <!-- Liste des projets -->
            <div v-if="loading" class="flex justify-center py-12">
                <Icon name="mdi:loading" class="w-8 h-8 animate-spin text-indigo-600" />
            </div>

            <div v-else-if="filteredProjects.length === 0" class="text-center py-12">
                <Icon name="mdi:folder-open" class="w-16 h-16 mx-auto text-gray-400" />
                <h3 class="mt-2 text-sm font-medium text-gray-900">Aucun projet</h3>
                <p class="mt-1 text-sm text-gray-500">
                    {{ user?.role === 'CTD'
                        ? 'Commencez par créer votre premier projet.'
                        : 'Aucun projet ne correspond à vos critères de recherche.' }}
                </p>
                <div v-if="user?.role === 'CTD'" class="mt-6">
                    <button @click="showProjectForm = true"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200">
                        <Icon name="mdi:plus" class="mr-2" />
                        Créer un projet
                    </button>
                </div>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <ProjectCard v-for="project in filteredProjects" :key="project.id" :project="project"
                    @accountability-submitted="refreshProjects" />
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="mt-6 flex justify-center">
                <nav class="flex items-center gap-2">
                    <button @click="page--" :disabled="page === 1" class="px-3 py-1 rounded border"
                        :class="page === 1 ? 'text-gray-400' : 'hover:bg-gray-100'">
                        Précédent
                    </button>

                    <span class="px-3 py-1">
                        Page {{ page }} sur {{ totalPages }}
                    </span>

                    <button @click="page++" :disabled="page === totalPages" class="px-3 py-1 rounded border"
                        :class="page === totalPages ? 'text-gray-400' : 'hover:bg-gray-100'">
                        Suivant
                    </button>
                </nav>
            </div>
        </div>

        <!-- Modal pour le formulaire de projet -->
        <Modal v-model="showProjectForm" :title="editingProject ? 'Modifier le projet' : 'Nouveau projet'" size="lg">
            <ProjectForm :project="editingProject" @submit="handleProjectSubmit" @cancel="closeProjectForm" />
        </Modal>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import type { Project, ProjectStatus } from '~/types'
import ProjectCard from '~/components/projects/ProjectCard.vue'
import ProjectForm from '~/components/projects/ProjectForm.vue'
import { useToast } from 'vue-toastification'
import { useAuth } from '~/composables/useAuth'

const toast = useToast()
const { user } = useAuth()

// Configuration de la page
definePageMeta({
    layout: 'dashboard',
    auth: true,
    middleware: ['auth']
})

// État
const projects = ref<Project[]>([])
const loading = ref(true)
const page = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')
const statusFilter = ref<ProjectStatus | ''>('')
const sortBy = ref('created_at')
const showProjectForm = ref(false)
const editingProject = ref<Project | undefined>(undefined)

// Constantes
const projectStatuses: ProjectStatus[] = ['PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SUSPENDED']
const PAGE_SIZE = 12

// Fonctions utilitaires
const getStatusLabel = (status: ProjectStatus): string => {
    const labels: Record<ProjectStatus, string> = {
        'PLANNED': 'Planifié',
        'IN_PROGRESS': 'En cours',
        'COMPLETED': 'Terminé',
        'SUSPENDED': 'Suspendu'
    }
    return labels[status]
}

// Projets filtrés
const filteredProjects = computed(() => {
    let result = [...projects.value]

    // Filtre par recherche
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(project =>
            project.title.toLowerCase().includes(query) ||
            project.description.toLowerCase().includes(query)
        )
    }

    // Filtre par statut
    if (statusFilter.value) {
        result = result.filter(project => project.status === statusFilter.value)
    }

    // Tri
    result.sort((a, b) => {
        const [field, order] = sortBy.value.startsWith('-')
            ? [sortBy.value.slice(1), -1]
            : [sortBy.value, 1]

        if (field === 'created_at') {
            return order * (new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        }
        if (field === 'title') {
            return order * a.title.localeCompare(b.title)
        }
        if (field === 'accountability_count') {
            return order * (b.accountability_count - a.accountability_count)
        }
        return 0
    })

    return result
})

// Chargement des projets
const fetchProjects = async () => {
    try {
        loading.value = true
        const token = localStorage.getItem('authToken')
        const response = await fetch(`http://localhost:8000/api/projects/?page=${page.value}&page_size=${PAGE_SIZE}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            throw new Error('Erreur lors du chargement des projets')
        }

        const data = await response.json()
        projects.value = data.results
        totalPages.value = Math.ceil(data.count / PAGE_SIZE)
    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Une erreur est survenue lors du chargement des projets')
    } finally {
        loading.value = false
    }
}

// Gestion du formulaire de projet
const handleProjectSubmit = async (formData: FormData) => {
    try {
        const url = editingProject.value
            ? `/api/projects/${editingProject.value.id}/update/`
            : '/api/projects/create/'

        const method = editingProject.value ? 'PATCH' : 'POST'

        const response = await fetch(url, {
            method,
            body: formData,
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
        })

        if (!response.ok) {
            throw new Error('Erreur lors de l\'enregistrement du projet')
        }

        toast.success(
            editingProject.value
                ? 'Le projet a été modifié avec succès'
                : 'Le projet a été créé avec succès'
        )

        closeProjectForm()
        fetchProjects()

    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Une erreur est survenue lors de l\'enregistrement du projet')
    }
}

const closeProjectForm = () => {
    showProjectForm.value = false
    editingProject.value = undefined
}

// Rafraîchir les projets
const refreshProjects = () => {
    fetchProjects()
}

// Surveillance des changements
watch([page], () => {
    fetchProjects()
})

// Initialisation
onMounted(() => {
    fetchProjects()
})
</script>
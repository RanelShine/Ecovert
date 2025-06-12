<!-- citoyenprojetsection -->
<template>
    <div class="space-y-6">
        <!-- Liste des projets -->
        <div class="bg-white rounded-lg shadow dark:bg-gray-600">
            <div class="p-6 border-b">
                <h2 class="text-3xl font-semibold text-green-700 text-center dark:text-green-600">Projets de la commune</h2>
            </div>
                <!-- Filtres et Tri -->
    <div class="bg-white p-4 rounded-lg shadow mb-6 dark:bg-gray-600">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Recherche -->
            <div class="relative">
                <input type="text" v-model="searchQuery" placeholder="Rechercher un projet..."
                    class="w-full pl-10 pr-4 py-2 border rounded-lg">
            </div>

            <!-- Filtre par statut -->
            <select v-model="statusFilter" class="w-full py-2 px-4 border rounded-lg">
                <option value="">Tous les statuts</option>
                <option v-for="status in projectStatuses" :key="status" :value="status">
                    {{ getStatutLabel(status) }}
                </option>
            </select>

            <!-- Tri -->
            <select v-model="sortBy" class="w-full py-2 px-4 border rounded-lg">
                <option value="created_at">Plus récents</option>
                <option value="-created_at">Plus anciens</option>
                <option value="title">Ordre alphabétique</option>
            </select>
        </div>
    </div>
            <div class="p-6">
                <div v-if="loading" class="text-center py-8">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p class="mt-4 text-gray-600">Chargement des projets...</p>
                </div>

                <div v-else-if="filteredAndSortedProjects.length === 0" class="text-center py-8">
                    <p class="text-gray-500">Aucun projet disponible pour le moment</p>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="projet in filteredAndSortedProjects" :key="projet.id" class="border rounded-lg p-4 dark:bg-gray-800">
                        <h3 class="font-semibold text-lg mb-2">{{ projet.title }}</h3>
                        <p class="text-gray-600 dark:text-white text-sm mb-4">{{ projet.description }}</p>
                        <div class="flex justify-between items-center">
                <span
                  :class="statusClass(projet.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium "
                >
                  {{ getStatutLabel(projet.status) }}
                </span>
                <span class="text-sm text-gray-500 dark:text-white">{{ formatDate(projet.start_date) }}</span>
              </div>
              <div class="mt-2">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300 dark:text-white"
                    :style="{ width: (projet.avancement || 0) + '%' }"
                  ></div>
                </div>
                <p class="text-xs text-gray-500 mt-1 dark:text-white">{{ projet.avancement || 0 }}% terminé</p>
              </div>
              <div class="mt-2">
                <p class="text-xs text-gray-500 dark:text-white">
                  Début : {{ formatDate(projet.start_date) }}<br />
                  Fin prévue : {{ projet.end_date ? formatDate(projet.end_date) : '—' }}
                </p>
              </div>
                         <!-- Bouton de téléchargement -->
              <div v-if="projet.file" class="mt-3">
                <button
                  @click.stop="downloadFile(projet.id, projet.title)"
                  class="w-full bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center justify-center"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Télécharger
                </button>
              </div>
                        <button @click="selectProjet(projet)"
                            class="text-indigo-600 hover:text-indigo-800 dark:text-green-400 dark:hover:text-green-600 text-sm font-medium">
                            Demander des comptes
                        </button>
                    </div>
                </div>
            </div>
        </div> 

        <!-- Formulaire de demande -->
        <div class="mb-6">
            <h1 class="text-2xl font-bold text-gray-900">Demande de comptes sur les projets</h1>
            <p class="mt-2 text-sm text-gray-600">Sélectionnez un projet et posez vos questions à la commune</p>
        </div>

        <!-- Formulaire de demande -->
        <div class="bg-white rounded-lg shadow p-6 dark:bg-gray-600">
            <form @submit.prevent="submitDemande" class="space-y-4">
                <!-- Sélection du projet -->
                <div>
                    <label for="projet" class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Projet concerné</label>
                    <select id="projet" v-model="form.projetId" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="">Sélectionnez un projet</option>
                        <option v-for="projet in projets" :key="projet.id" :value="projet.id">
                        {{ projet.title }}
                        </option>
                    </select>

                </div>

                <!-- Question/Demande -->
                <div>
                    <label for="question" class="block dark:text-white text-sm font-medium text-gray-700 mb-1">Votre question ou
                        demande</label>
                    <textarea id="question" v-model="form.question" rows="4" required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="Décrivez votre demande de comptes concernant ce projet..."></textarea>
                </div>

                <!-- Bouton de soumission -->
                <div class="flex justify-end">
                    <button type="submit" :disabled="submitting"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
                        <span v-if="submitting" class="mr-2">
                            <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                </path>
                            </svg>
                        </span>
                        {{ submitting ? 'Envoi en cours...' : 'Envoyer la demande' }}
                    </button>
                </div>
            </form>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const searchQuery = ref('');
const statusFilter = ref<Projet['status'] | ''>(''); 
const sortBy = ref('created_at');
const page = ref(1);
const totalPages = ref(1);
const PAGE_SIZE = 12;
const API_BASE_URL = 'http://localhost:8000'

interface Projet {
  id: number;
  title: string;
  description: string;
  status: 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'SUSPENDED';
  start_date: string;
  end_date: string | null;
  budget: number;
  avancement: number;
  file: string | null;
  created_at?: string;
}

const projets = ref<Projet[]>([])
const loading = ref(false)
const submitting = ref(false)
const form = ref({
    projetId: '',
    question: ''
})

const fetchProjets = async () => {
    loading.value = true
    try {
        const params = new URLSearchParams({
            page: page.value.toString(),
            page_size: PAGE_SIZE.toString(),
            search: searchQuery.value,
            ordering: sortBy.value,
        });

        // Ajouter le filtre de statut seulement s'il n'est pas vide
        if (statusFilter.value) {
            params.append('status', statusFilter.value);
        }

        const response = await fetch(`${API_BASE_URL}/api/projects/?${params.toString()}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) throw new Error('Erreur lors du chargement des projets')

        const data = await response.json()
        if (data && Array.isArray(data.results)) {
             projets.value = data.results;
             totalPages.value = Math.ceil(data.count / PAGE_SIZE);
             console.log('Projets chargés (paginé):', projets.value);
        } else if (data && Array.isArray(data)) {
             projets.value = data;
             totalPages.value = 1;
             console.log('Projets chargés (liste directe):', projets.value);
        } else {
             console.error('Format de données API inattendu pour les projets:', data);
             projets.value = [];
             toast.error('Format de données API inattendu lors du chargement des projets.');
        }

    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Erreur lors du chargement des projets')
        projets.value = [];
    } finally {
        loading.value = false
    }
}

const selectProjet = (projet: Projet) => {
    form.value.projetId = String(projet.id)
    document.querySelector('#projet')?.scrollIntoView({ behavior: 'smooth' })
}

const formatCurrency = (value: number) =>
  new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'XOF' }).format(value);

const formatDate = (date: string) => {
    if (!date) return '—';
    const dateObj = new Date(date);
    if (isNaN(dateObj.getTime())) {
        console.warn('Date invalide reçue:', date);
        return 'Date invalide';
    }
    return dateObj.toLocaleDateString('fr-FR');
}

const projectStatuses: Projet['status'][] = ['PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SUSPENDED'];

const statusClass = (status: Projet['status']) => {
  switch (status) {
    case 'PLANNED':
      return 'bg-gray-200 text-gray-700';
    case 'IN_PROGRESS':
      return 'bg-yellow-200 text-yellow-800';
    case 'COMPLETED':
      return 'bg-green-200 text-green-800';
    case 'SUSPENDED':
      return 'bg-red-200 text-red-800';
    default:
        return 'bg-gray-200 text-gray-700';
  }
};

const getStatutLabel = (status: Projet['status']) => {
  const labels: Record<Projet['status'], string> = {
    'PLANNED': 'Planifié',
    'IN_PROGRESS': 'En cours',
    'COMPLETED': 'Terminé',
    'SUSPENDED': 'Suspendu'
  };
  return labels[status] || status;
};

// Fonction de filtrage et tri côté client
const filteredAndSortedProjects = computed(() => {
  let result = [...projets.value];

  // Filtrage par recherche
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(projet => 
      projet.title.toLowerCase().includes(query) ||
      projet.description.toLowerCase().includes(query)
    );
  }

  // Filtrage par statut
  if (statusFilter.value) {
    result = result.filter(projet => projet.status === statusFilter.value);
  }

  // Tri
  switch (sortBy.value) {
    case 'created_at':
      result.sort((a, b) => {
        const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
        const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
        return dateB - dateA;
      });
      break;
    case '-created_at':
      result.sort((a, b) => {
        const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
        const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
        return dateA - dateB;
      });
      break;
    case 'title':
      result.sort((a, b) => a.title.localeCompare(b.title));
      break;
  }

  return result;
});

// Soumettre la demande
const submitDemande = async () => {
    submitting.value = true
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

        if (!response.ok) {
             const errorData = await response.json(); 
             console.error('Erreur lors de l\'envoi de la demande:', response.status, response.statusText, errorData);
             throw new Error(`Erreur lors de l\'envoi de la demande: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`);
        }

        toast.success('Votre demande a été envoyée avec succès')
        // Réinitialiser le formulaire
        form.value = {
            projetId: '',
            question: ''
        }
    } catch (error) {
        console.error('Erreur:', error)
        if (error instanceof Error && error.message.includes('Erreur lors de l\'envoi de la demande:')) {
             toast.error(error.message);
        } else {
             toast.error('Erreur lors de l\'envoi de la demande');
        }
    } finally {
        submitting.value = false
    }
}

const downloadFile = async (projectId: number, projectTitle: string) => {
  try {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}/download/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // Récupérer le nom du fichier depuis les headers
    const contentDisposition = response.headers.get('Content-Disposition');
    let fileName = `${projectTitle.replace(/[^a-zA-Z0-9]/g, '_')}_document`;
    
    if (contentDisposition) {
      const fileNameMatch = contentDisposition.match(/filename="(.+)"/);
      if (fileNameMatch) {
        fileName = fileNameMatch[1];
      }
    }
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    toast.success('Téléchargement démarré');
  } catch (error) {
    console.error('Erreur lors du téléchargement:', error);
    toast.error('Erreur lors du téléchargement du fichier');
  }
};

onMounted(() => {
    fetchProjets()
})

// Watch pour les changements de filtres - ne recharge que si nécessaire
watch([searchQuery, statusFilter, sortBy], () => {
  // Pour la recherche et le tri, on peut utiliser le filtrage côté client
  // Seule la pagination pourrait nécessiter un rechargement
  page.value = 1; // Reset la page quand on change les filtres
  
  // Optionnel: recharger depuis l'API si vous préférez le filtrage côté serveur
  // fetchProjets();
});

watch(page, () => {
  fetchProjets();
});
</script>
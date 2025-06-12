<!-- CTDProjetSection -->
<template>
  <div class="space-y-6">
    <!-- Header avec bouton d'ajout -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-green-700 dark:text-green-600">Gestion des Projets</h1>
      <button
        @click="openAddModal"
        class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
      >
        + Nouveau Projet
      </button>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white p-6 rounded-lg shadow-md dark:bg-gray-600">
        <h3 class="text-sm font-medium text-gray-500 dark:text-green-400">Total Projets</h3>
        <p class="text-3xl font-bold text-blue-600">{{ stats.total }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md dark:bg-gray-600">
        <h3 class="text-sm font-medium text-gray-500 dark:text-green-400">En Cours</h3>
        <p class="text-3xl font-bold text-yellow-600">{{ stats.enCours }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md dark:bg-gray-600">
        <h3 class="text-sm font-medium text-gray-500 dark:text-green-400">Terminés</h3>
        <p class="text-3xl font-bold text-pink-600">{{ stats.termines }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md dark:bg-gray-600 ">
        <h3 class="text-sm font-medium text-gray-500 dark:text-green-400">Budget Total</h3>
        <p class="text-3xl font-bold text-purple-600">{{ formatCurrency(stats.budgetTotal) }}</p>
      </div>
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

    <!-- Liste des projets -->
    <div class="bg-white rounded-lg shadow-md dark:bg-gray-600">
      <div class="p-6 border-b">
        <h2 class="text-3xl font-semibold text-center text-green-700 dark:text-green-600">Liste des Projets</h2>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Chargement des projets...</p>
        </div>

        <div v-else-if="!loading && projets.length === 0" class="text-center py-8">
          <h3 class="mt-2 text-sm font-medium text-gray-900">Aucun projet</h3>
          <p class="mt-1 text-sm text-gray-500">
              Commencez par créer votre premier projet.
          </p>
           <div class="mt-6">
                <button @click="openAddModal"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200">
                    Créer un projet
                </button>
            </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="projet in filteredAndSortedProjects"
            :key="projet.id"
            class="border rounded-lg p-4 hover:shadow-lg dark:bg-gray-800 transition-shadow cursor-pointer"
            @click="selectProjet(projet)"
          >
            <div class="space-y-2">
              <h3 class="font-semibold text-lg">{{ projet.title }}</h3>
              <p class="text-gray-600 dark:text-white text-sm line-clamp-2">{{ projet.description }}</p>
              
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
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-6 flex justify-center">
        <nav class="flex items-center gap-2">
            <button @click="page--" :disabled="page === 1" class="px-3 py-1 rounded border"
                :class="page === 1 ? 'text-gray-400 cursor-not-allowed' : 'hover:bg-gray-100'">
                Précédent
            </button>

            <span class="px-3 py-1">
                Page {{ page }} sur {{ totalPages }}
            </span>

            <button @click="page++" :disabled="page === totalPages" class="px-3 py-1 rounded border"
                :class="page === totalPages ? 'text-gray-400 cursor-not-allowed' : 'hover:bg-gray-100'">
                Suivant
            </button>
        </nav>
    </div>

    <!-- Modal d'ajout / modification -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold dark:text-green-600">
            {{ selectedProjet ? 'Modifier le Projet' : 'Nouveau Projet' }}
          </h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitProjet" class="space-y-4">
          <input v-model="form.id" type="hidden" />

          <div>
            <label class="block text-sm dark:text-white font-medium text-gray-700 mb-1">Titre du projet</label>
            <input v-model="form.title" type="text" required class="input" />
          </div>

          <div>
            <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Description</label>
            <textarea v-model="form.description" required rows="3" class="input"></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm dark:text-white font-medium text-gray-700 mb-1">Budget (FCFA)</label>
              <input v-model.number="form.budget" type="number" required min="0" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Statut</label>
              <select v-model="form.status" required class="input">
                <option value="PLANNED">Planifié</option>
                <option value="IN_PROGRESS">En cours</option>
                <option value="COMPLETED">Terminé</option>
                <option value="SUSPENDED">Suspendu</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Date de début</label>
              <input v-model="form.start_date" type="date" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Date de fin prévue</label>
              <input v-model="form.end_date" type="date" class="input" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Avancement (%)</label>
            <input v-model.number="form.avancement" type="number" min="0" max="100" required class="input" />
          </div>

          <!-- Champ fichier modifié pour accepter tous les types -->
          <div>
            <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Fichier joint</label>
            <input @change="handleFileUpload" type="file" class="input" />
            <p class="text-xs text-gray-500 mt-1">Tous types de fichiers acceptés (images, documents, etc.)</p>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="closeModal" class="btn-cancel">Annuler</button>
            <button v-if="selectedProjet" type="button"  @click="deleteProjet" class="btn-delete bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium" :disabled="submitting">
              {{ submitting ? 'Suppression...' : 'Supprimer' }}
            </button>
            <button type="submit" :disabled="submitting" class="btn-primary">
              {{ submitting ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';


const toast = useToast();

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

interface ProjetForm extends Partial<Projet> {
    uploadedFile?: File | null;
}

// Données réactives
const projets = ref<Projet[]>([]);
const selectedProjet = ref<Projet | null>(null);
const showAddModal = ref(false);
const loading = ref(false);
const submitting = ref(false);

const searchQuery = ref('');
const statusFilter = ref<Projet['status'] | ''>(''); 
const sortBy = ref('created_at');
const page = ref(1);
const totalPages = ref(1);
const PAGE_SIZE = 12;

const stats = reactive({
  total: 0,
  enCours: 0,
  termines: 0,
  budgetTotal: 0,
});

const form = reactive<ProjetForm>({
  id: undefined,
  title: '',
  description: '',
  budget: 0,
  status: 'PLANNED',
  start_date: '',
  end_date: '',
  avancement: 0,
  file: null, // Changé de 'file_url' à 'file'
  uploadedFile: null,
});

const projectStatuses: Projet['status'][] = ['PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SUSPENDED'];

// Nouvelles fonctions utilitaires pour les fichiers
const isImage = (fileUrl: string): boolean => {
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'];
  return imageExtensions.some(ext => fileUrl.toLowerCase().includes(ext));
};

const getFileName = (fileUrl: string): string => {
  return fileUrl.split('/').pop() || 'Fichier';
};

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

// Fonction pour charger les projets
const fetchProjects = async () => {
  loading.value = true;
  try {
    const params = {
      page: page.value,
      page_size: PAGE_SIZE,
      search: searchQuery.value,
      status: statusFilter.value,
      ordering: sortBy.value,
    };

    const token = localStorage.getItem('authToken');

    const response = await axios.get('http://127.0.0.1:8000/api/projects/', {
      params,
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.data) {
        let projectsData: Projet[] = [];
        let totalCount = 0;

        if (Array.isArray(response.data)) {
            projectsData = response.data;
            totalCount = response.data.length; 
            totalPages.value = 1; 
            console.warn('API renvoie une liste non paginée pour les projets.');
        } else if (Array.isArray(response.data.results) && typeof response.data.count === 'number') {
            projectsData = response.data.results;
            totalCount = response.data.count;
            totalPages.value = Math.ceil(totalCount / PAGE_SIZE);
        } else {
            console.error('Format de données API inattendu pour les projets:', response.data);
            toast.error('Format de données API inattendu lors du chargement des projets.');
        }

        projets.value = projectsData;
        updateStats(); 

    } else {
        console.error('Réponse API vide lors du chargement des projets.');
        projets.value = [];
        totalPages.value = 0;
        updateStats();
        toast.error('Réponse API vide lors du chargement des projets.');
    }

  } catch (error) {
    console.error('Erreur lors du chargement des projets:', error);
    projets.value = [];
    totalPages.value = 0;
    updateStats();
    toast.error('Une erreur est survenue lors du chargement des projets');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProjects();
});

watch([searchQuery, statusFilter, sortBy, page], () => {
  fetchProjects();
});

// Fonctions utilitaires
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

const getStatutLabel = (status: Projet['status']) => {
  const labels: Record<Projet['status'], string> = {
    'PLANNED': 'Planifié',
    'IN_PROGRESS': 'En cours',
    'COMPLETED': 'Terminé',
    'SUSPENDED': 'Suspendu'
  };
  return labels[status] || status;
};

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

// Méthodes
const openAddModal = () => {
  selectedProjet.value = null;
  Object.assign(form, {
    id: undefined,
    title: '',
    description: '',
    budget: 0,
    status: 'PLANNED',
    start_date: '',
    end_date: '',
    avancement: 0,
    file: null, // Changé de 'file_url' à 'file'
    uploadedFile: null,
  });
  showAddModal.value = true;
};

const closeModal = () => {
  showAddModal.value = false;
  selectedProjet.value = null;
};

// Fonction modifiée pour gérer tous types de fichiers
const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    form.uploadedFile = file;

    // Pour les images, on peut toujours afficher un aperçu
    if (isImage(file.name)) {
      const reader = new FileReader();
      reader.onload = (e) => {
        form.file = e.target?.result as string; // Changé de 'file_url' à 'file'
      };
      reader.readAsDataURL(file);
    } else {
      // Pour les autres fichiers, on stocke juste le nom
      form.file = file.name; // Changé de 'file_url' à 'file'
    }
  } else {
    form.uploadedFile = null;
    if (form.id === undefined) {
        form.file = null; // Changé de 'file_url' à 'file'
    }
  }
};

const selectProjet = (projet: Projet) => {
  selectedProjet.value = projet;
  const formattedProjet = {
      ...projet,
      start_date: projet.start_date ? projet.start_date.split('T')[0] : '',
      end_date: projet.end_date ? projet.end_date.split('T')[0] : '',
      file: projet.file, // Changé de 'file_url' à 'file'
  };
  Object.assign(form, formattedProjet);
  form.uploadedFile = null;
  showAddModal.value = true;
};

const submitProjet = async () => {
  submitting.value = true;
  try {
    const formData = new FormData();
    Object.keys(form).forEach(key => {
        if (key === 'file' || key === 'uploadedFile') return; 

        const value = form[key as keyof ProjetForm]; 
        if (key === 'id' && value === undefined) return;

        if (value !== null && value !== undefined) {
             if (key === 'start_date' || key === 'end_date') {
                 if (value instanceof Date) {
                     formData.append(key, value.toISOString().split('T')[0]);
                 } else if (typeof value === 'string' && value) {
                      formData.append(key, value);
                 }
             }
             else {
                formData.append(key, value.toString());
             }
        }
    });

    if (form.uploadedFile instanceof File) {
        formData.append('file', form.uploadedFile);
    }

    let response: any;
    const token = localStorage.getItem('authToken');

    if (form.id !== undefined) {
      response = await axios.patch(`http://127.0.0.1:8000/api/projects/${form.id}/update/`, formData, {
           headers: {
                'Authorization': `Bearer ${token}`,
           },
      });
      const index = projets.value.findIndex(p => p.id === response.data.id);
      if (index !== -1) {
        projets.value[index] = { ...projets.value[index], ...response.data };
      }
      toast.success('Le projet a été modifié avec succès');

    } else {
      response = await axios.post('http://127.0.0.1:8000/api/projects/create/', formData, {
           headers: {
                'Authorization': `Bearer ${token}`,
           },
      });

      projets.value.push(response.data);
      toast.success('Le projet a été créé avec succès');
    }

    closeModal();
    fetchProjects();

  } catch (error) {
    console.error("Erreur lors de la soumission du projet:", error);
    if (axios.isAxiosError(error) && error.response) {
        console.error("Détails de l'erreur API:", error.response.data);
        let errorMessage = 'Erreur lors de l\'enregistrement: ';
        if (error.response.data) {
            try {
                errorMessage += JSON.stringify(error.response.data);
            } catch (e) {
                errorMessage += 'Détails non disponibles.';
            }
        }
        toast.error(errorMessage);
    } else {
        toast.error("Une erreur est survenue lors de l'enregistrement du projet");
    }
  } finally {
    submitting.value = false;
  }
};

const updateStats = () => {
  stats.total = projets.value.length; 
  stats.enCours = projets.value.filter(p => p.status === 'IN_PROGRESS').length;
  stats.termines = projets.value.filter(p => p.status === 'COMPLETED').length;
  stats.budgetTotal = projets.value.reduce((sum, p) => sum + (p.budget || 0), 0);
};

const deleteProjet = async () => {
  if (!form.id) return;

  if (!confirm("Êtes-vous sûr de vouloir supprimer ce projet ?")) {
    return;
  }

  submitting.value = true;

  try {

    const token = localStorage.getItem('authToken');
   await axios.delete(`/api/projects/${selectedProjet.value?.id}/delete/`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});


    // Retirer le projet supprimé de la liste
    projets.value = projets.value.filter(p => p.id !== form.id);

    toast.success("Projet supprimé avec succès.");
    closeModal();
  } catch (error) {
    console.error(error);
    toast.error("Erreur lors de la suppression du projet.");
  } finally {
    submitting.value = false;
  }
};

const filteredAndSortedProjects = computed(() => {
  let result = [...projets.value]

    switch (sortBy.value) {
    case 'created_at':
      result.sort((a, b) => {
        const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
        const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
        return dateB - dateA;
      });
      break
    case '-created_at':
      result.sort((a, b) => {
        const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
        const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
        return dateA - dateB;
      });
      break
    case 'title':
      result.sort((a, b) => a.title.localeCompare(b.title))
      break
  }

  return result
})

</script>

<style scoped>
.input {
  width: 100%;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  outline: none;
  transition: box-shadow 0.2s;
}
.input:focus {
  box-shadow: 0 0 0 2px #3b82f6;
  border-color: #3b82f6;
}

.btn-cancel {
  padding-left: 1rem;
  padding-right: 1rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  color: #374151;
  background-color: #e5e7eb;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}
.btn-cancel:hover {
  background-color: #d1d5db;
}

.btn-primary {
  padding-left: 1rem;
  padding-right: 1rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  background-color: #2563eb;
  color: #fff;
  border-radius: 0.375rem;
  transition: background-color 0.2s, opacity 0.2s;
}
.btn-primary:hover {
  background-color: #1d4ed8;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
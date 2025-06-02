<template>
  <div class="space-y-6">
    <!-- Header avec bouton d'ajout -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Gestion des Projets</h1>
      <button
        @click="openAddModal"
        class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
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

    <!-- Filtres et Tri -->
    <div class="bg-white p-4 rounded-lg shadow mb-6">
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
    <div class="bg-white rounded-lg shadow-md">
      <div class="p-6 border-b">
        <h2 class="text-xl font-semibold">Mes Projets</h2>
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
            v-for="projet in projets"
            :key="projet.id"
            class="border rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer"
            @click="selectProjet(projet)"
          >
            <div v-if="projet.image" class="mb-4">
              <img
                :src="projet.image"
                alt="Image du projet"
                class="w-full h-48 object-cover rounded-lg"
              />
            </div>
            <div class="space-y-2">
              <h3 class="font-semibold text-lg">{{ projet.title }}</h3>
              <p class="text-gray-600 text-sm line-clamp-2">{{ projet.description }}</p>
              <div class="flex justify-between items-center">
                <span
                  :class="statusClass(projet.status)"
                  class="px-2 py-1 rounded-full text-xs font-medium"
                >
                  {{ getStatutLabel(projet.status) }}
                </span>
                <span class="text-sm text-gray-500">{{ formatDate(projet.start_date) }}</span>
              </div>
              <div class="mt-2">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: (projet.avancement || 0) + '%' }"
                  ></div>
                </div>
                <p class="text-xs text-gray-500 mt-1">{{ projet.avancement || 0 }}% terminé</p>
              </div>
              <div class="mt-2">
                <p class="text-xs text-gray-500">
                  Début : {{ formatDate(projet.start_date) }}<br />
                  Fin prévue : {{ projet.end_date ? formatDate(projet.end_date) : '—' }}
                </p>
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
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">
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
            <label class="block text-sm font-medium text-gray-700 mb-1">Titre du projet</label>
            <input v-model="form.title" type="text" required class="input" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="form.description" required rows="3" class="input"></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Budget (XOF)</label>
              <input v-model.number="form.budget" type="number" required min="0" class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Statut</label>
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
              <label class="block text-sm font-medium text-gray-700 mb-1">Date de début</label>
              <input v-model="form.start_date" type="date" required class="input" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Date de fin prévue</label>
              <input v-model="form.end_date" type="date" class="input" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Avancement (%)</label>
            <input v-model.number="form.avancement" type="number" min="0" max="100" required class="input" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Image</label>
            <input @change="handleImageUpload" type="file" accept="image/*" class="input" />
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="closeModal" class="btn-cancel">Annuler</button>
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
import { ref, reactive, onMounted, watch } from 'vue';
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
  image: string | null; 
  created_at?: string;
}

interface ProjetForm extends Partial<Projet> {
    imageFile?: File | null; 
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

// Utiliser le nouveau type ProjetForm
const form = reactive<ProjetForm>({
  id: undefined,
  title: '',
  description: '',
  budget: 0,
  status: 'PLANNED',
  start_date: '',
  end_date: '',
  avancement: 0,
  image: null, 
  imageFile: null, 
});

const projectStatuses: Projet['status'][] = ['PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SUSPENDED'];


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
            // Format liste directe 
            projectsData = response.data;
            totalCount = response.data.length; 
            totalPages.value = 1; 
            console.warn('API renvoie une liste non paginée pour les projets.');
        } else if (Array.isArray(response.data.results) && typeof response.data.count === 'number') {
            // Format paginé (DRF par défaut)
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
    image: null,
    imageFile: null, 
  });
  showAddModal.value = true;
};

const closeModal = () => {
  showAddModal.value = false;
  selectedProjet.value = null;
};

const handleImageUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    form.imageFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
      form.image = e.target?.result as string; 
    };
    reader.readAsDataURL(file);
  } else {
    form.imageFile = null;
    if (form.id === undefined) {
        form.image = null;
    }
  }
};

const selectProjet = (projet: Projet) => {
  selectedProjet.value = projet;
  const formattedProjet = {
      ...projet,
      start_date: projet.start_date ? projet.start_date.split('T')[0] : '',
      end_date: projet.end_date ? projet.end_date.split('T')[0] : '',
      image: projet.image, 
  };
  Object.assign(form, formattedProjet);
  form.imageFile = null; 
  showAddModal.value = true;
};


const submitProjet = async () => {
  submitting.value = true;
  try {
    const formData = new FormData();
    Object.keys(form).forEach(key => {
        if (key === 'image' || key === 'imageFile') return;

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

    if (form.imageFile instanceof File) {
        formData.append('image', form.imageFile);
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
</style>
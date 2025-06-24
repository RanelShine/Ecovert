<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-green-700 dark:text-green-600">Gestion des Projets</h1>
      <button
        @click="openAddModal"
        class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
      >
        + Nouveau Projet
      </button>
    </div>

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

    <div class="bg-white p-4 rounded-lg shadow mb-6 dark:bg-gray-600">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="relative">
                <input type="text" v-model="searchQuery" placeholder="Rechercher un projet..."
                    class="w-full pl-10 pr-4 py-2 border rounded-lg">
            </div>

            <select v-model="statusFilter" class="w-full py-2 px-4 border rounded-lg">
                <option value="">Tous les statuts</option>
                <option v-for="status in projectStatuses" :key="status" :value="status">
                    {{ getStatutLabel(status) }}
                </option>
            </select>

            <select v-model="sortBy" class="w-full py-2 px-4 border rounded-lg">
                <option value="created_at">Plus récents</option>
                <option value="-created_at">Plus anciens</option>
                <option value="title">Ordre alphabétique</option>
            </select>
        </div>
    </div>

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
            class="border rounded-lg p-4 hover:shadow-lg dark:bg-gray-800 transition-shadow"
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
              
              <div class="flex justify-end items-center mt-3">
                <div class="">
                  <button @click.stop="openCommentsModal(projet)"
                  class="text-blue-600 hover:text-blue-800 dark:text-green-400 dark:hover:text-green-600 text-sm font-medium flex items-center">
                  Commentaires
                </button>
                </div>
                 <button @click.stop="deleteProjet(projet)"
                    class="p-2 rounded-full text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900 transition-colors"
                    title="Supprimer le projet">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                </button>
                <button @click.stop="openEditModal(projet)"
                    class="p-2 rounded-full text-blue-600 hover:bg-blue-100 dark:text-blue-400 dark:hover:bg-blue-900 transition-colors"
                    title="Modifier le projet">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                    </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

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

    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold dark:text-green-600">
            {{ selectedProjet ? `Modifier le Projet: ${selectedProjet.title}` : 'Nouveau Projet' }}
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

          <div>
            <label class="block text-sm font-medium dark:text-white text-gray-700 mb-1">Fichier joint</label>
            <input @change="handleFileUpload" type="file" class="input" />
            <p class="text-xs text-gray-500 mt-1">Tous types de fichiers acceptés (images, documents, etc.)</p>
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

    <div v-if="showCommentsModal && selectedProjetForComments"
       class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col dark:bg-gray-700">
      <div class="p-6 border-b flex justify-between items-center border-gray-200 dark:border-gray-600">
        <h3 class="text-2xl font-semibold text-gray-800 dark:text-white">
          Commentaires pour "{{ selectedProjetForComments.title }}"
        </h3>
        <button @click="closeCommentsModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-100">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-6 overflow-y-auto flex-grow">
        <div class="mb-6">
          <h4 class="text-xl font-medium text-gray-800 mb-3 dark:text-white">Ajouter un commentaire</h4>
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <img class="h-10 w-10 rounded-full object-cover" 
                   :src="currentUserAvatar" 
                   :alt="currentUserInitial">
            </div>
            <div class="flex-grow">
              <textarea v-model="newCommentText"
                        placeholder="Écrivez votre commentaire ici..."
                        class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white dark:border-gray-600"
                        rows="3"></textarea>
              <p v-if="loadingComments" class="text-sm text-gray-500 mt-1 dark:text-gray-400">
                Chargement des commentaires existants...
              </p>
              <div class="mt-2 text-right">
                <button @click="submitComment"
                        :disabled="!newCommentText.trim() || commenting"
                        class="bg-green-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 dark:text-white-400 dark:hover:text-white-600 dark:bg-green-500 dark:hover:bg-green-600">
                  <span v-if="commenting" class="mr-2">
                    <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </span>
                  {{ commenting ? 'Envoi...' : 'Commenter' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <h4 class="text-xl font-medium text-gray-800 mb-3 dark:text-white">Tous les commentaires</h4>
          <div v-if="loadingComments" class="text-center py-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2 text-gray-600 dark:text-gray-300">Chargement des commentaires...</p>
          </div>
          <div v-else-if="!loadingComments && commentsForSelectedProjet && commentsForSelectedProjet.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400">
            Aucun commentaire pour ce projet. Soyez le premier !
          </div>
          <div v-else class="space-y-4">
            <div v-for="comment in commentsForSelectedProjet" :key="comment.id"
                 class="bg-gray-50 p-4 rounded-lg dark:bg-gray-800 dark:text-white dark:border-gray-700">
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <img class="h-8 w-8 rounded-full object-cover" 
                        :src="comment.author?.avatar || 'https://placehold.co/32x32/cccccc/ffffff?text=U'" 
                        :alt="comment.author?.prenom ? comment.author.prenom[0].toUpperCase() : 'U'">
                </div>
                <div class="flex-grow">
                  <div class="flex justify-between items-center mb-1">
                    <span class="font-semibold text-gray-900 dark:text-white">
                      {{ comment.author?.prenom || comment.author?.nom ? (comment.author.prenom || '') + ' ' + (comment.author.nom || '') : comment.author?.email || 'Utilisateur inconnu' }}
                    </span>
                    <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatTimeAgo(comment.created_at) }}</span>
                  </div>
                  <p class="text-gray-700 dark:text-gray-300">{{ comment.text }}</p>
                  <div class="mt-2 flex space-x-3 text-sm text-gray-500 dark:text-gray-400">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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

interface Comment {
  id: number;
  project: number;
  author: {
    id: number;
    email: string;
    nom?: string;
    prenom?: string;
    avatar: string;
  };
  text: string;
  created_at: string;
  updated_at: string;
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
const API_BASE_URL = 'http://localhost:8000'

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

const showCommentsModal = ref(false);
const selectedProjetForComments = ref<Projet | null>(null);
const commentsForSelectedProjet = ref<Comment[]>([]);
const newCommentText = ref('');
const loadingComments = ref(false);
const commenting = ref(false);

// Nouveau : État de l'utilisateur actuel (pour l'avatar et le nom dans la section d'ajout de commentaire)
const currentUser = ref<{
  id: number;
  email: string;
  nom?: string;
  prenom?: string;
  avatar?: string;
} | null>(null);

// Propriétés calculées pour l'avatar de l'utilisateur actuel
const currentUserAvatar = computed(() => {
  if (currentUser.value?.avatar) { // Si un champ avatar direct existe sur currentUser
    return currentUser.value.avatar;
  }
  // Logique pour générer un avatar factice similaire à votre backend
  const initial = currentUser.value?.prenom ? currentUser.value.prenom[0].toUpperCase() : 
                               currentUser.value?.nom ? currentUser.value.nom[0].toUpperCase() : 
                               currentUser.value?.email ? currentUser.value.email[0].toUpperCase() : 'U';
  return `https://placehold.co/40x40/cccccc/ffffff?text=${initial}`;
});

const currentUserInitial = computed(() => {
  return currentUser.value?.prenom ? currentUser.value.prenom[0].toUpperCase() : 
           currentUser.value?.nom ? currentUser.value.nom[0].toUpperCase() : 
           currentUser.value?.email ? currentUser.value.email[0].toUpperCase() : 'U';
});

const openCommentsModal = async (projet: Projet) => {
  selectedProjetForComments.value = projet;
  showCommentsModal.value = true;
  loadingComments.value = true; 
  commentsForSelectedProjet.value = []; // Vider les anciens commentaires pour un nouveau chargement

  try {
    const token = localStorage.getItem('authToken');
    if (!token) { 
      toast.error("Vous devez être connecté pour voir les commentaires.");
      loadingComments.value = false; // Assurez-vous que l'état de chargement est désactivé même ici
      return; 
    }

    const response = await fetch(`${API_BASE_URL}/api/projects/${projet.id}/comments/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Erreur lors du chargement des commentaires:', response.status, response.statusText, errorData);
      toast.error('Erreur lors du chargement des commentaires.');
      return; 
    }

    // Assurez-vous que la réponse est bien un tableau avant de l'assigner
    const data = await response.json();
    console.log('Commentaires reçus du backend :', data);
    commentsForSelectedProjet.value = Array.isArray(data.results) ? data.results : [];



  } catch (error) {
    console.error('Erreur (catch) lors du chargement des commentaires:', error);
    toast.error('Une erreur inattendue est survenue lors du chargement.');
  } finally {
    loadingComments.value = false; // TRÈS IMPORTANT : S'assure que l'état de chargement est désactivé
  }
};

const closeCommentsModal = () => {
  showCommentsModal.value = false;
  selectedProjetForComments.value = null;
  commentsForSelectedProjet.value = [];
  newCommentText.value = '';
};

const submitComment = async () => {
  if (!newCommentText.value.trim() || !selectedProjetForComments.value) {
    return; 
  }

  commenting.value = true; 

  try {
    const token = localStorage.getItem('authToken');
    if (!token) { 
        toast.error("Vous devez être connecté pour laisser un commentaire.");
        commenting.value = false; // Assurez-vous que l'état d'envoi est désactivé
        return;
    }

    const response = await fetch(`${API_BASE_URL}/api/projects/${selectedProjetForComments.value.id}/comments/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        project: selectedProjetForComments.value.id, 
        text: newCommentText.value
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Erreur lors de l\'envoi du commentaire:', response.status, response.statusText, errorData);
      toast.error(`Erreur lors de l'envoi du commentaire: ${JSON.stringify(errorData.detail || errorData)}`);
      return; 
    }

    const newComment = await response.json();
    commentsForSelectedProjet.value.unshift(newComment); 
    newCommentText.value = ''; 
    toast.success('Votre commentaire a été ajouté avec succès !');

  } catch (error) {
    // Correction de l'erreur de syntaxe: utilisation de guillemets doubles ou échappement
    console.error("Erreur générale lors de l'envoi du commentaire:", error);
    toast.error("Une erreur inattendue est survenue lors de l'envoi.");
  } finally {
    commenting.value = false; // TRÈS IMPORTANT : S'assure que l'état d'envoi est désactivé
  }
};

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

const formatTimeAgo = (timestamp: string): string => {
  const now = new Date();
  const date = new Date(timestamp);
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return `${seconds} seconde${seconds === 1 ? '' : 's'} ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} heure${hours === 1 ? '' : 's'} ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days} jour${days === 1 ? '' : 's'} ago`;
  
  // Si plus d'une semaine, afficher la date complète
  return date.toLocaleDateString('fr-FR');
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

// Propriété calculée pour le filtrage et le tri
const filteredAndSortedProjects = computed(() => {
  let filtered = projets.value;

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(projet => 
      projet.title.toLowerCase().includes(query) ||
      projet.description.toLowerCase().includes(query)
    );
  }

  if (statusFilter.value) {
    filtered = filtered.filter(projet => projet.status === statusFilter.value);
  }

  return filtered.sort((a, b) => {
    if (sortBy.value === 'title') {
      return a.title.localeCompare(b.title);
    } else if (sortBy.value === 'created_at') {
      return new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime();
    } else if (sortBy.value === '-created_at') {
      return new Date(a.created_at || '').getTime() - new Date(b.created_at || '').getTime();
    }
    return 0;
  });
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

const openEditModal = (projet: Projet) => {
  selectedProjet.value = projet;
  const formattedProjet = {
      ...projet,
      start_date: projet.start_date ? projet.start_date.split('T')[0] : '',
      end_date: projet.end_date ? projet.end_date.split('T')[0] : '',
      file: projet.file,
  };
  Object.assign(form, formattedProjet);
  form.uploadedFile = null;
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
        form.file = e.target?.result as string; 
      };
      reader.readAsDataURL(file);
    } else {
      // Pour les autres fichiers, on stocke juste le nom
      form.file = file.name; 
    }
  } else {
    form.uploadedFile = null;
    if (form.id === undefined) {
        form.file = null; 
    }
  }
};

const submitProjet = async () => {
  submitting.value = true;
  try {
    const formData = new FormData();
    Object.keys(form).forEach(key => {
        if (key === 'file' && !form.uploadedFile) return; // Ne pas envoyer le champ 'file' si un nouveau fichier n'a pas été sélectionné
        if (key === 'uploadedFile') return; // Ne pas ajouter 'uploadedFile' directement à formData

        const value = form[key as keyof ProjetForm]; 
        if (value !== undefined && value !== null) { // Seulement ajouter les valeurs définies et non nulles
            if (key === 'start_date' || key === 'end_date') {
                // S'assurer que les dates sont envoyées au format attendu par le backend (ex: YYYY-MM-DD)
                formData.append(key, value as string);
            } else {
                formData.append(key, String(value));
            }
        }
    });

    if (form.uploadedFile) {
        formData.append('file', form.uploadedFile);
    }

    const token = localStorage.getItem('authToken');
    if (!token) {
        toast.error("Vous devez être connecté.");
        submitting.value = false;
        return;
    }

    let response;
    if (form.id) {
        // Modification
        response = await axios.patch(`${API_BASE_URL}/api/projects/${form.id}/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data', 
            },
        });
        toast.success('Projet modifié avec succès !');
    } else {
        // Ajout
        response = await axios.post(`${API_BASE_URL}/api/projects/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
        });
        toast.success('Projet ajouté avec succès !');
    }
    
    closeModal();
    fetchProjects(); 
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement du projet:', error);
    if (axios.isAxiosError(error) && error.response) {
      if (error.response.status === 400) {
        toast.error('Erreur de validation: ' + JSON.stringify(error.response.data));
      } else if (error.response.status === 401) {
        toast.error('Non autorisé. Veuillez vous connecter.');
      } else {
        toast.error('Erreur lors de l\'enregistrement : ' + (error.response.data.detail || error.message));
      }
    } else {
      toast.error('Une erreur inattendue est survenue.');
    }
  } finally {
    submitting.value = false;
  }
};

const deleteProjet = async (projetToDelete: Projet) => {
  if (!confirm(`Êtes-vous sûr de vouloir supprimer le projet "${projetToDelete.title}" ? Cette action est irréversible.`)) {
    return;
  }

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      toast.error("Vous devez être connecté pour supprimer un projet.");
      return;
    }

    await axios.delete(`${API_BASE_URL}/api/projects/${projetToDelete.id}/delete/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    toast.success('Projet supprimé avec succès !');
    closeModal(); // Ferme la modale si elle était ouverte pour le projet supprimé
    fetchProjects(); // Rafraîchit la liste des projets
  } catch (error) {
    console.error('Erreur lors de la suppression du projet:', error);
    if (axios.isAxiosError(error) && error.response) {
      toast.error('Erreur lors de la suppression : ' + (error.response.data.detail || error.message));
    } else {
      toast.error('Une erreur inattendue est survenue lors de la suppression.');
    }
  }
};

const updateStats = () => {
  stats.total = projets.value.length;
  stats.enCours = projets.value.filter(p => p.status === 'IN_PROGRESS').length;
  stats.termines = projets.value.filter(p => p.status === 'COMPLETED').length;
  stats.budgetTotal = projets.value.reduce((sum, p) => sum + p.budget, 0);
};
</script>

<style scoped>
.input {
  @apply w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white;
}
.btn-primary {
  @apply bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50;
}
.btn-cancel {
  @apply bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg font-medium transition-colors;
}
</style>
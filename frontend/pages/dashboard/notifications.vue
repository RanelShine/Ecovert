
<template>
  <div class="max-w-6xl mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Notifications et Demandes</h1>

    <!-- Affichage conditionnel basé sur le rôle de l'utilisateur -->
    <div v-if="user?.role === 'ctd'">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">Demandes de comptes reçues</h2>

      <!-- Liste des demandes -->
      <div v-if="loadingRequests" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Chargement des demandes...</p>
      </div>

      <div v-else-if="accountabilityRequests.length === 0" class="text-center py-8">
        <p class="text-gray-500">Aucune demande de comptes reçue pour le moment.</p>
      </div>

      <div v-else class="space-y-6">
        <div v-for="request in accountabilityRequests" :key="request.id" class="bg-white rounded-lg shadow p-6 border border-gray-200">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Projet: {{ request.project?.title || 'N/A' }}</h3>
              <p class="text-gray-700 mb-4"><strong>Demande:</strong> {{ request.question }}</p>
              <p v-if="request.response" class="text-green-700 mt-2"><strong>Réponse:</strong> {{ request.response }}</p>
              <p v-else class="text-yellow-700 mt-2">En attente de réponse.</p>
            </div>
            <button
              @click="openResponseModal(request)"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              {{ request.response ? 'Modifier la réponse' : 'Répondre' }}
            </button>
          </div>
          <p class="text-sm text-gray-500 mt-4">Reçue le: {{ formatDate(request.created_at) }}</p>
        </div>
      </div>
    </div>

    <!-- Message pour les autres rôles -->
    <div v-else>
      <p class="text-gray-700">Bienvenue sur votre page de notifications. Les fonctionnalités spécifiques à votre rôle seront disponibles ici prochainement.</p>
      <!-- Vous pouvez ajouter d'autres contenus ou messages ici pour les autres rôles -->
    </div>

    <!-- Modal de réponse -->
    <div
      v-if="showResponseModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">
            {{ selectedRequest?.response ? 'Modifier la réponse' : 'Répondre à la demande' }}
          </h2>
          <button @click="closeResponseModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="selectedRequest" class="mb-4">
            <p class="text-sm font-medium text-gray-700">Projet:</p>
            <p class="text-base text-gray-900 font-semibold">{{ selectedRequest.project?.title || 'N/A' }}</p>
            <p class="text-sm font-medium text-gray-700 mt-2">Demande:</p>
            <p class="text-base text-gray-800">{{ selectedRequest.question }}</p>
        </div>


        <form @submit.prevent="submitResponse" class="space-y-4">
          <div>
            <label for="response" class="block text-sm font-medium text-gray-700 mb-1">Votre réponse</label>
            <textarea
              id="response"
              v-model="responseForm.responseText"
              rows="6"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Écrivez votre réponse ici..."
            ></textarea>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="closeResponseModal" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100">Annuler</button>
            <button type="submit" :disabled="submittingResponse" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
              <span v-if="submittingResponse" class="mr-2">
                <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ selectedRequest?.response ? 'Modifier' : 'Envoyer la réponse' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useState } from '#app'; // Importez useState de Nuxt 3

const toast = useToast();
const API_BASE_URL = 'http://localhost:8000'; // Assurez-vous que cette URL est correcte

interface User {
  role?: string;

}

const user = useState<User>('user');

definePageMeta({
  layout: 'dashboard',
  auth: true,
  middleware: ['auth']
});


interface AccountabilityRequest {
  id: number;
  project: { 
    id: number;
    title: string;

  } | null;
  question: string;
  response: string | null; 
  created_at: string;
}

// Données réactives
const accountabilityRequests = ref<AccountabilityRequest[]>([]);
const loadingRequests = ref(false);
const selectedRequest = ref<AccountabilityRequest | null>(null);
const showResponseModal = ref(false);
const submittingResponse = ref(false);

const responseForm = reactive({
  responseText: '',
});


const fetchAccountabilityRequests = async () => {
  if (user.value?.role !== 'ctd') {
    console.log('Utilisateur non CTD, ne charge pas les demandes de comptes.');
    accountabilityRequests.value = []; 
    return;
  }

  loadingRequests.value = true;
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
        console.warn('Aucun token trouvé, impossible de charger les demandes.');
        accountabilityRequests.value = [];
        toast.error('Authentification requise pour charger les demandes.');
        return;
    }


    const response = await axios.get(`${API_BASE_URL}/api/projects/accountability/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });


    if (Array.isArray(response.data)) {
        accountabilityRequests.value = response.data;
        console.log('Demandes chargées:', accountabilityRequests.value);
    } else if (response.data && Array.isArray(response.data.results)) {
         accountabilityRequests.value = response.data.results;
         console.log('Demandes chargées (paginé):', accountabilityRequests.value);

    }
    else {
        console.error('Format de données API inattendu pour les demandes:', response.data);
        accountabilityRequests.value = [];
        toast.error('Format de données API inattendu lors du chargement des demandes.');
    }


  } catch (error) {
    console.error('Erreur lors du chargement des demandes:', error);
    accountabilityRequests.value = []; 
    toast.error('Une erreur est survenue lors du chargement des demandes');
  } finally {
    loadingRequests.value = false;
  }
};

// Fonction pour ouvrir la modale de réponse
const openResponseModal = (request: AccountabilityRequest) => {
  selectedRequest.value = request;
  responseForm.responseText = request.response || '';
  showResponseModal.value = true;
};

// Fonction pour fermer la modale de réponse
const closeResponseModal = () => {
  showResponseModal.value = false;
  selectedRequest.value = null;
  responseForm.responseText = ''; 
};

// Fonction pour soumettre la réponse
const submitResponse = async () => {
  if (!selectedRequest.value) return; 

  submittingResponse.value = true;
  try {
    const token = localStorage.getItem('authToken');
     if (!token) {
        console.warn('Aucun token trouvé, impossible de soumettre la réponse.');
        toast.error('Authentification requise pour répondre.');
        return;
    }

   
    const response = await axios.post(`${API_BASE_URL}/api/projects/accountability/${selectedRequest.value.id}/respond/`, {
      response: responseForm.responseText,
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 200 || response.status === 201) {
        toast.success('Réponse envoyée avec succès');
        closeResponseModal();
        fetchAccountabilityRequests(); 
    } else {

         console.warn('Réponse API inattendue lors de la soumission de la réponse:', response.status, response.data);
         toast.warning('Réponse soumise, mais la confirmation API est inattendue.');
         closeResponseModal();
         fetchAccountabilityRequests(); 
    }


  } catch (error) {
    console.error('Erreur lors de la soumission de la réponse:', error);
     if (axios.isAxiosError(error) && error.response) {
        console.error("Détails de l'erreur API:", error.response.data);
        let errorMessage = 'Erreur lors de l\'envoi de la réponse: ';
        if (error.response.data) {
            try {
                errorMessage += JSON.stringify(error.response.data);
            } catch (e) {
                errorMessage += 'Détails non disponibles.';
            }
        }
        toast.error(errorMessage);
    } else {
        toast.error('Une erreur est survenue lors de l\'envoi de la réponse');
    }
  } finally {
    submittingResponse.value = false;
  }
};

// Fonction utilitaire pour formater la date
const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A';
    try {
        const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleDateString('fr-FR', options);
    } catch (e) {
        console.error('Erreur de formatage de date:', dateString, e);
        return 'Date invalide';
    }
};



onMounted(() => {

  fetchAccountabilityRequests();
});

</script>

<style scoped>

</style>

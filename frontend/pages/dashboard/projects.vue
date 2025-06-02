<template>
    <div class="min-h-screen bg-gray-100">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <!-- Affichage conditionnel seulement après hydratation -->
            <div v-if="isHydrated">
                <!-- CTD -->
                <div v-if="userRole === 'ctd'">
                    <CTDProjectSection />
                </div>

                <!-- Citoyens -->
                <div v-else-if="userRole === 'citoyen'">
                    <CitoyenProjectSection />
                </div>

                <!-- ONG ou entreprise -->
                <div v-else-if="userRole === 'entreprise' || userRole === 'ong'">
                    <EntrepriseProjectSection />
                </div>

                <!-- Fallback si aucun rôle ne correspond -->
                <div v-else>
                    <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                        <p class="text-red-600">⚠️ Rôle utilisateur non reconnu: <strong>{{ userRole }}</strong></p>
                        <p class="text-sm text-red-500 mt-2">Affichage par défaut ou message d'erreur.</p>
                    </div>
                    <!--  choisir d'afficher une section par défaut ou un message -->
                    <!-- <CitoyenProjectSection /> -->
                </div>
            </div>

            <!-- Loading pendant l'hydratation -->
            <div v-else class="flex justify-center items-center py-12">
                <div class="text-gray-500 flex items-center space-x-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-500"></div>
                    <span>Chargement des données utilisateur...</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import CTDProjectSection from '~/components/sections/projets/CTDProjetSection.vue' 
import CitoyenProjectSection from '~/components/sections/projets/CitoyenProjetSection.vue'
import EntrepriseProjectSection from '~/components/sections/projets/EntrepriseProjetSection.vue'
// Configuration de la page
definePageMeta({
    layout: 'dashboard',
    auth: true, 
    middleware: ['auth']
})


const userRole = ref<string>('')
const isHydrated = ref<boolean>(false)

const fetchUserDataFromAPI = async (): Promise<any> => {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            console.log('[projects.vue] Pas de token trouvé');
            return null;
        }

        const response = await fetch('http://localhost:8000/api/accounts/me/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const userData = await response.json();
            console.log('[projects.vue] Données utilisateur API:', userData);
            return userData;
        } else {
             console.error('[projects.vue] Erreur API lors de la récupération utilisateur:', response.status, response.statusText);
             // Gérer les erreurs 
             if (response.status === 401) {
                 console.log('[projects.vue] Token probablement expiré ou invalide, déconnexion...');
                
             }
             return null;
        }
    } catch (error) {
        console.error('[projects.vue] Erreur fetchUserDataFromAPI:', error);
        return null;
    }
};

const getUserRole = async (): Promise<string> => {
    try {
        console.log('[projects.vue] Début de getUserRole');

        // Essayer d'abord les données du localStorage 
        const localUserData = localStorage.getItem('userData');
        let userData = null;

        if (localUserData) {
            try {
                userData = JSON.parse(localUserData);
                console.log('[projects.vue] userData localStorage:', userData);
            } catch (parseError) {
                console.error('[projects.vue] Erreur parsing localStorage:', parseError);
            }
        }

        // Si pas de données locales valides ou pas de rôle, récupérer depuis l'API
        if (!userData || !userData.role) {
            console.log('[projects.vue] Récupération depuis l\'API nécessaire');
            userData = await fetchUserDataFromAPI();
        }

        if (userData && userData.role) {
            const role = userData.role.toLowerCase().trim();
            console.log(`[projects.vue] Role final déterminé: "${role}"`);

            // Vérifier que le rôle est valide
            const validRoles = ['citoyen', 'ctd', 'ong', 'entreprise'];
            if (!validRoles.includes(role)) {
                console.warn(`[projects.vue] Role invalide "${role}", utilisation de "citoyen" par défaut`);
                return 'citoyen'; 
            }

            return role;
        }

        console.log('[projects.vue] Aucune donnée utilisateur valide trouvée - retour citoyen par défaut');
        return 'citoyen'; 

    } catch (error) {
        console.error('[projects.vue] Erreur dans getUserRole:', error);
        return 'citoyen'; 
    }
};


onMounted(async () => {
    console.log('[projects.vue] Composant monté - début de l\'initialisation');
    await nextTick();
    console.log('[projects.vue] NextTick terminé');

    userRole.value = await getUserRole();
    isHydrated.value = true;

    console.log(`[projects.vue] Initialisation terminée - Role final: "${userRole.value}"`);
});


</script>

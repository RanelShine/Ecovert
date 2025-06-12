<template>
<div class="min-h-screen flex items-start justify-center bg-gray-50 pt-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">

      <!-- Étape 1 : formulaire d’inscription -->
      <div v-if="step === 1">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-gray-900">
            Créer un compte
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Ou
            <NuxtLink to="/auth/login" class="font-medium text-green-600 hover:text-green-500">
              se connecter avec un compte existant
            </NuxtLink>
          </p>
        </div>
        <form class="mt-2 bg-green-100 p-7 rounded-xl space-y-6" @submit.prevent="register">
          <div class="rounded-md shadow-sm -space-y-px">
            <!-- Email -->
            <div class="relative">
              <input
                id="email-address"
                name="email"
                type="email"
                required
                v-model="formData.email"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Adresse e-mail"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M16 12H8m8 0l-4-4m4 4l-4 4"/>
                </svg>
              </div>
            </div>

            <!-- Nom -->
            <div class="relative">
              <input
                id="name"
                name="name"
                type="text"
                required
                v-model="formData.nom"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Nom"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M5.121 17.804A6 6 0 0112 15a6 6 0 016.879 2.804M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
            </div>

            <!-- Prénom -->
            <div class="relative">
              <input
                id="surname"
                name="surname"
                type="text"
                required
                v-model="formData.prenom"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Prénom"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </div>
            </div>

            <!-- Téléphone -->
            <div class="relative">
              <input
                id="phone"
                name="phone"
                type="tel"
                required
                v-model="formData.telephone"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Téléphone"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 5a2 2 0 012-2h3.28a1 1 0 01.949.684l1.32 3.956a1 1 0 01-.217 1.01l-2.457 2.457a11.042 11.042 0 005.292 5.292l2.457-2.457a1 1 0 011.01-.217l3.956 1.32a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C8.268 21 3 15.732 3 9V5z"/>
                </svg>
              </div>
            </div>

            <!-- Rôle -->
            <div class="relative">
              <select
                id="role"
                name="role"
                required
                v-model="formData.role"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              >
                <option disabled value="">Sélectionnez un rôle</option>
                <option value="ctd">CTD</option>
                <option value="ONG">ONG</option>
                <option value="Entreprise">Entreprise</option>
                <option value="Citoyens">Citoyen</option>
              </select>
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12h6m2 4H7a2 2 0 01-2-2V7a2 2 0 012-2h3.5l1-1h2l1 1H17a2 2 0 012 2v7a2 2 0 01-2 2z"/>
                </svg>
              </div>
            </div>

            <!-- Commune -->
            <div class="relative">
              <select
                id="commune"
                name="commune"
                required
                v-model="formData.commune"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              >
                <option disabled value="">Sélectionnez une commune</option>
                <option v-for="c in communes" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
            </div>

            <!-- Mots de passe -->
            <div class="relative">
              <input
                id="password"
                name="password"
                type="password"
                required
                v-model="formData.password"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Mot de passe"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 11c.828 0 1.5.672 1.5 1.5S12.828 14 12 14s-1.5-.672-1.5-1.5S11.172 11 12 11zM5 11V9a7 7 0 0114 0v2m-2 0v7a2 2 0 01-2 2H9a2 2 0 01-2-2v-7h10z"/>
                </svg>
              </div>
            </div>
            <div class="relative">
              <input
                id="password-confirm"
                name="password-confirm"
                type="password"
                required
                v-model="passwordConfirm"
                class="appearance-none mb-4 block w-full pl-10 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Confirmer le mot de passe"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M5 13l4 4L19 7"/>
                </svg>
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              :disabled="authStore.loading"
            >
              <span v-if="authStore.loading">Chargement…</span>
              <span v-else>Valider</span>
            </button>
          </div>

          <div v-if="errorMessage" class="text-red-600 text-center">
            {{ errorMessage }}
          </div>
        </form>
      </div>

      <!-- Étape 2 : saisie du code -->
      <div v-else-if="step === 2" class="mt-6 p-6 bg-yellow-50 rounded-xl">
        <h3 class="font-bold text-lg mb-4">Code de vérification</h3>
        <p>Un code à 6 chiffres vous a été envoyé à <strong>{{ emailUsed }}</strong>.</p>
        <input
          v-model="verificationCode"
          type="text"
          maxlength="6"
          placeholder="Entrez le code reçu"
          class="mt-4 w-full p-2 border rounded"
        />
        <button
          @click="verifyCode"
          class="mt-4 w-full py-2 px-4 rounded text-white bg-green-600 hover:bg-green-700"
          :disabled="authStore.loading"
        >
          <span v-if="authStore.loading">Vérification…</span>
          <span v-else>Vérifier</span>
        </button>
      </div>

      <!-- Étape 3 : succès -->
      <div v-else class="mt-6 bg-green-100 p-7 rounded-xl space-y-6">
        <div class="text-center text-green-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-green-500" fill="none"
               viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-xl font-bold mt-2">Inscription et activation réussies !</h3>
          <p class="mt-2">Votre compte est activé, vous pouvez désormais vous connecter.</p>
          <button
            @click="goToLogin"
            class="mt-4 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            Aller à la page de connexion
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore, useCommunes } from '~/stores/auth';

const router     = useRouter();
const authStore = useAuthStore();
const { getCommunes } = useCommunes();

// Étapes : 1 = inscription, 2 = vérification, 3 = succès
const step             = ref(1);

const formData         = ref({
  email: '', nom: '', prenom: '', telephone: '', role: '', commune: '', password: ''
});
const passwordConfirm  = ref('');
const communes         = ref<{ id: number; name: string }[]>([]);
const emailUsed        = ref('');
const verificationCode = ref('');

// Gestion des erreurs
const localError = ref<string | null>(null);
const errorMessage = computed(() => {
  if (localError.value) return localError.value;
  if (!authStore.error) return null;
  if (typeof authStore.error === 'object') {
    const first = Object.values(authStore.error)[0];
    return Array.isArray(first) ? first[0] : first;
  }
  return authStore.error;
});

// Charger les communes (exemple statique)
onMounted(async () => {
  communes.value = [
    { id: 1, name: 'Bafoussam I' },
    { id: 2, name: 'Bafoussam II' },
    { id: 3, name: 'Mandjou' }
  ];
  // ou : communes.value = await getCommunes();
});
const register = async () => {
  if (formData.value.password !== passwordConfirm.value) {
    localError.value = "Les mots de passe ne correspondent pas";
    return;
  }
  localError.value = null;
  try {
    await authStore.register({ ...formData.value });
    emailUsed.value = formData.value.email;
    step.value      = 2;
  } catch (err) {
    console.error(err);
  }
};

// 2️⃣ Vérification du code
const verifyCode = async () => {
  try {
    const res = await authStore.verifyAccount({
      email: emailUsed.value,
      code:  verificationCode.value
    });
    if (res.success) {
      step.value = 3;
    } else {
      alert(res.message || 'Code invalide ou expiré.');
    }
  } catch (err) {
    console.error(err);
    alert('Erreur lors de la vérification.');
  }
};

// 3️⃣ Aller à la connexion
const goToLogin = () => {
  router.push('/auth/login');
};
</script>

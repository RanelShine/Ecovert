import { useAuthStore } from '~/stores/auth';

export default defineNuxtPlugin(({ app }) => {
  // Initialisation de l'authentification au démarrage de l'application
  if (process.client) {
    const authStore = useAuthStore();
    authStore.initAuth();
  }
});
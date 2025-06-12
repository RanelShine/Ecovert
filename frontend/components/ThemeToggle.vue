<!-- components/ThemeToggle.vue -->
<template>
  <div class="theme-toggle">
    <button 
      @click="toggleTheme"
      class="theme-btn"
      :class="{ 'dark-mode': theme === 'dark' }"
      :title="theme === 'light' ? 'Passer en mode sombre' : 'Passer en mode clair'"
    >
      <!-- Icône soleil pour le mode clair -->
      <svg 
        v-if="theme === 'light'" 
        xmlns="http://www.w3.org/2000/svg" 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
        fill="none" 
        stroke="currentColor" 
        stroke-width="2"
      >
        <circle cx="12" cy="12" r="5"/>
        <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
      </svg>
      
      <!-- Icône lune pour le mode sombre -->
      <svg 
        v-else 
        xmlns="http://www.w3.org/2000/svg" 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
        fill="none" 
        stroke="currentColor" 
        stroke-width="2"
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
    </button>

    <!-- Sélecteur de thème avec options multiples (optionnel) -->
    <!-- <select 
      v-model="currentTheme" 
      @change="handleThemeChange"
      class="theme-select"
      v-if="showSelect"
    >
      <option value="light">🌞 Clair</option>
      <option value="dark">🌙 Sombre</option>
    </select> -->
  </div>
</template>

<script setup lang="ts">
interface Props {
  showSelect?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showSelect: false
})

const { theme, toggleTheme, setTheme, initTheme } = useTheme()

const currentTheme = computed({
  get: () => theme.value,
  set: (value: 'light' | 'dark') => setTheme(value)
})

const handleThemeChange = (event: Event) => {
  const target = event.target as HTMLSelectElement
  setTheme(target.value as 'light' | 'dark')
}

// Initialiser le thème au montage du composant
onMounted(() => {
  initTheme()
})
</script>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.theme-btn {
  padding: 0.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  background-color: #ffffff;
  color: #374151;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-btn:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1;
  transform: scale(1.05);
}

.theme-btn.dark-mode {
  background-color: #1f2937;
  color: #f9fafb;
  border-color: #4b5563;
}

.theme-btn.dark-mode:hover {
  background-color: #374151;
  border-color: #6b7280;
}

.theme-select {
  padding: 0.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  background-color: #ffffff;
  color: #374151;
  cursor: pointer;
}

/* Styles pour le mode sombre */
:global(.dark) .theme-select {
  background-color: #1f2937;
  color: #f9fafb;
  border-color: #4b5563;
}
</style>
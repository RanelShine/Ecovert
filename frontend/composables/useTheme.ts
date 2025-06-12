// composables/useTheme.ts
export const useTheme = () => {
  // État réactif pour le thème actuel
  const theme = useState<'light' | 'dark'>('theme', () => 'light')

  // Fonction pour basculer entre les thèmes
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    applyTheme(theme.value)
    // Sauvegarder dans localStorage si côté client
    if (process.client) {
      localStorage.setItem('theme', theme.value)
    }
  }

  // Fonction pour définir un thème specific
  const setTheme = (newTheme: 'light' | 'dark') => {
    theme.value = newTheme
    applyTheme(newTheme)
    if (process.client) {
      localStorage.setItem('theme', newTheme)
    }
  }

  // Fonction pour appliquer le thème au DOM
  const applyTheme = (currentTheme: 'light' | 'dark') => {
    if (process.client) {
      const html = document.documentElement
      if (currentTheme === 'dark') {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
    }
  }

  // Initialiser le thème au chargement
  const initTheme = () => {
    if (process.client) {
      // Récupérer le thème sauvegardé ou utiliser la préférence système
      const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      
      const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light')
      setTheme(initialTheme)
    }
  }

  return {
    theme: readonly(theme),
    toggleTheme,
    setTheme,
    initTheme
  }
}
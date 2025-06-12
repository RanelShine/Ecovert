// plugins/theme.client.ts
export default defineNuxtPlugin(() => {
  // Ne s'exécute que côté client
  if (process.client) {
    const { initTheme } = useTheme()
    
    // Initialiser le thème dès que possible
    initTheme()
    
    // Écouter les changements de préférence système
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      // Seulement si aucun thème n'est sauvegardé
      if (!localStorage.getItem('theme')) {
        const { setTheme } = useTheme()
        setTheme(e.matches ? 'dark' : 'light')
      }
    })
  }
})
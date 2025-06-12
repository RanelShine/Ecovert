<!-- <template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div>
</template> -->

<template>
  <!-- <div :class="[themeClass, 'min-h-screen']"></div> -->
  <div class="min-h-screen">
    <NuxtLayout>
      <div id="app" :class="themeClass">
      <NuxtPage />
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import type { Theme } from '~/composables/useTheme'

// Utiliser le composable de thème
const { theme, initTheme } = useTheme()

// Classe CSS réactive basée sur le thème
const themeClass = computed(() => theme.value)

// Initialiser le thème côté client
onMounted(() => {
  initTheme()
})

// Gérer le thème côté serveur avec les cookies
const themeCookie = useCookie<Theme>('theme', {
  default: () => 'light' as Theme
})

// Synchroniser le thème avec le cookie
watch(theme, (newTheme) => {
  themeCookie.value = newTheme
}, { immediate: true })

// Configuration du head pour éviter le flash
useHead({
  htmlAttrs: {
    'data-theme': theme,
    class: theme
  },
  bodyAttrs: {
    'data-theme': theme,
    class: theme
  }
})
</script>

<style>
#app {
  min-height: 100vh;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>
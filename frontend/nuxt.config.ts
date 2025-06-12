// https://nuxt.com/docs/api/configuration/nuxt-config
import process from 'node:process';
export default defineNuxtConfig({
  css: ['@/assets/css/tailwind.css', '~/assets/css/theme.css'],
  compatibilityDate: '2024-11-01',
  devtools: {
    enabled: true
  },
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxtjs/color-mode',
    '@vueuse/nuxt'
  ],
  colorMode: {
    preference: 'light', // mode préféré
    fallback: 'light',   // mode de secours si rien n'est défini
    classSuffix: ''      // pas de suffixe, donc class="dark" ou class="light"
  },  // <-- Il manquait cette virgule ici
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
    configPath: 'tailwind.config.js'
  },
  app: {
    head: {
      title: 'Redevabilité Verte',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          key: 'description',
          name: 'description',
          content: 'Plateforme de redevabilité environnementale pour les communes'
        }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    },
    pageTransition: { name: 'page', mode: 'out-in' }
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/api',
      recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY || '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' // Clé reCAPTCHA de test
    }
  },
  router: {
    options: {
      strict: true
    }
  },
  experimental: {
    payloadExtraction: false
  }
})


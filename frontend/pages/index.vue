<template>
    <div>
      <div class="relative bg-green-600 overflow-hidden">
        <div class="max-w-7xl mx-auto">
          <div class="relative z-10 pb-8 bg-green-600 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <div class="pt-10 sm:pt-16 lg:pt-8 xl:pt-16">
              <div class="sm:text-center lg:text-left">
                <h1 class="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
                  <span class="block">Plateforme de</span>
                  <span class="block text-green-200">Redevabilité Verte</span>
                </h1>
                <p class="mt-3 text-base text-green-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Une plateforme collaborative où citoyens, administrations locales, entreprises et ONG peuvent interagir pour contribuer à une gestion plus responsable de l'environnement.
                </p>
                <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  <div class="rounded-md shadow">
                    <NuxtLink to="/auth/register" class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-green-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10">
                      Participer
                    </NuxtLink>
                  </div>
                  <div class="mt-3 sm:mt-0 sm:ml-3">
                    <NuxtLink to="/about" class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-green-500 hover:bg-green-400 md:py-4 md:text-lg md:px-10">
                      En savoir plus
                    </NuxtLink>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2 bg-green-500">
          <!-- Image placeholder -->
          <div class="h-56 w-full sm:h-72 md:h-96 lg:w-full lg:h-full bg-green-400 flex items-center justify-center">
            <span class="text-white text-5xl font-bold">🌱</span>
          </div>
        </div>
      </div>
  
      <div class="py-12 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="lg:text-center">
            <h2 class="text-base text-green-600 font-semibold tracking-wide uppercase">Fonctionnalités</h2>
            <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Une meilleure gestion environnementale
            </p>
            <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
              Des outils pour suivre, signaler et améliorer la gestion environnementale dans votre commune.
            </p>
          </div>
  
          <div class="mt-10">
            <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
              <div class="flex">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-12 w-12 rounded-md bg-green-500 text-white">
                    <!-- Heroicon name: outline/chart-bar -->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Tableau de bord interactif</h3>
                  <p class="mt-2 text-base text-gray-500">
                    Suivez les indicateurs environnementaux tels que la qualité de l'air, la gestion des déchets et la consommation d'eau.
                  </p>
                </div>
              </div>
  
              <div class="flex">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-12 w-12 rounded-md bg-green-500 text-white">
                    <!-- Heroicon name: outline/speakerphone -->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Signalement citoyen</h3>
                  <p class="mt-2 text-base text-gray-500">
                    Signalez des problèmes environnementaux comme la pollution, la déforestation illégale ou la mauvaise gestion des déchets.
                  </p>
                </div>
              </div>
  
              <div class="flex">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-12 w-12 rounded-md bg-green-500 text-white">
                    <!-- Heroicon name: outline/light-bulb -->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Transparence des acteurs</h3>
                  <p class="mt-2 text-base text-gray-500">
                    Accédez aux rapports d'impact écologique des administrations locales et aux engagements environnementaux des entreprises.
                  </p>
                </div>
              </div>
  
              <div class="flex">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-12 w-12 rounded-md bg-green-500 text-white">
                    <!-- Heroicon name: outline/chat-alt -->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Questions/Réponses</h3>
                  <p class="mt-2 text-base text-gray-500">
                    Posez vos questions environnementales et obtenez des réponses des autorités locales, entreprises et ONG.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  definePageMeta({
    layout: 'default'
  })
  </script>
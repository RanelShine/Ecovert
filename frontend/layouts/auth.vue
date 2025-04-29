<!-- frontend/layouts/auth.vue -->

<template>
    <div class="min-h-screen flex flex-col bg-gray-50">
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex">
              <NuxtLink to="/" class="flex-shrink-0 flex items-center">
                <span class="text-green-600 text-xl font-bold">Redevabilité Verte</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </header>
  
      <main class="flex-grow flex items-center justify-center">
        <div class="max-w-md w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <slot />
        </div>
      </main>
  
      <footer class="bg-white border-t border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p class="text-center text-sm text-gray-500">&copy; {{ new Date().getFullYear() }} Redevabilité Verte. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  </template>
<template>
    <div class="min-h-screen bg-gray-100">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 ">
            <div class="mb-6">
                <h1 class="text-3xl font-bold text-gray-900">
                    Carte des Signalements
                </h1>
                <p class="mt-2 text-sm text-gray-600">
                    Visualisez les signalements en cours et en attente sur la carte
                </p>
            </div>

            <MapSection :key="route.fullPath" />
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import MapSection from '@/components/sections/signalement/MapSection.vue'

// Configuration de la page
definePageMeta({
    layout: 'dashboard',
    auth: true,
    middleware: ['auth']
})

const route = useRoute()
</script>
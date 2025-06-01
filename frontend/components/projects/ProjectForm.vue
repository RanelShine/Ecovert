<template>
    <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Titre -->
        <div>
            <label for="title" class="block text-sm font-medium text-gray-700">
                Titre du projet *
            </label>
            <input id="title" v-model="form.title" type="text" required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                :class="{ 'border-red-500': errors.title }">
            <p v-if="errors.title" class="mt-1 text-sm text-red-600">
                {{ errors.title }}
            </p>
        </div>

        <!-- Description -->
        <div>
            <label for="description" class="block text-sm font-medium text-gray-700">
                Description détaillée *
            </label>
            <textarea id="description" v-model="form.description" rows="4" required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                :class="{ 'border-red-500': errors.description }"></textarea>
            <p v-if="errors.description" class="mt-1 text-sm text-red-600">
                {{ errors.description }}
            </p>
        </div>

        <!-- Statut -->
        <div>
            <label for="status" class="block text-sm font-medium text-gray-700">
                État du projet *
            </label>
            <select id="status" v-model="form.status" required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                :class="{ 'border-red-500': errors.status }">
                <option v-for="status in projectStatuses" :key="status" :value="status">
                    {{ getStatusLabel(status) }}
                </option>
            </select>
            <p v-if="errors.status" class="mt-1 text-sm text-red-600">
                {{ errors.status }}
            </p>
        </div>

        <!-- Dates -->
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
                <label for="start_date" class="block text-sm font-medium text-gray-700">
                    Date de début
                </label>
                <input id="start_date" v-model="form.start_date" type="date"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    :class="{ 'border-red-500': errors.start_date }">
                <p v-if="errors.start_date" class="mt-1 text-sm text-red-600">
                    {{ errors.start_date }}
                </p>
            </div>

            <div>
                <label for="end_date" class="block text-sm font-medium text-gray-700">
                    Date de fin prévue
                </label>
                <input id="end_date" v-model="form.end_date" type="date"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    :class="{ 'border-red-500': errors.end_date }">
                <p v-if="errors.end_date" class="mt-1 text-sm text-red-600">
                    {{ errors.end_date }}
                </p>
            </div>
        </div>

        <!-- Budget -->
        <div>
            <label for="budget" class="block text-sm font-medium text-gray-700">
                Budget alloué (€)
            </label>
            <input id="budget" v-model.number="form.budget" type="number" min="0" step="0.01"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                :class="{ 'border-red-500': errors.budget }">
            <p v-if="errors.budget" class="mt-1 text-sm text-red-600">
                {{ errors.budget }}
            </p>
        </div>

        <!-- Image -->
        <div>
            <label class="block text-sm font-medium text-gray-700">
                Image du projet
            </label>
            <div class="mt-1 flex items-center">
                <img v-if="imagePreview" :src="imagePreview" alt="Aperçu" class="h-32 w-32 object-cover rounded-lg">
                <div v-else
                    class="h-32 w-32 flex items-center justify-center rounded-lg border-2 border-dashed border-gray-300">
                    <Icon name="mdi:image" class="h-8 w-8 text-gray-400" />
                </div>

                <input type="file" ref="fileInput" @change="handleImageChange" accept="image/*" class="hidden">

                <button type="button" @click="triggerFileInput"
                    class="ml-4 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">
                    Changer l'image
                </button>

                <button v-if="imagePreview" type="button" @click="removeImage"
                    class="ml-2 px-3 py-2 text-sm font-medium text-red-600 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">
                    Supprimer
                </button>
            </div>
            <p v-if="errors.image" class="mt-1 text-sm text-red-600">
                {{ errors.image }}
            </p>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-4">
            <button type="button" @click="$emit('cancel')"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">
                Annuler
            </button>

            <button type="submit" :disabled="isSubmitting"
                class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
                <span v-if="isSubmitting" class="flex items-center gap-2">
                    <Icon name="mdi:loading" class="animate-spin" />
                    Enregistrement...
                </span>
                <span v-else>
                    {{ project ? 'Modifier' : 'Créer' }} le projet
                </span>
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Project, ProjectStatus } from '~/types'

const props = defineProps<{
    project?: Project
}>()

const emit = defineEmits<{
    (e: 'submit', project: FormData): void
    (e: 'cancel'): void
}>()

// État
const form = reactive({
    title: props.project?.title || '',
    description: props.project?.description || '',
    status: props.project?.status || 'PLANNED' as ProjectStatus,
    start_date: props.project?.start_date || '',
    end_date: props.project?.end_date || '',
    budget: props.project?.budget || null,
    image: null as File | null
})

const errors = reactive<Record<string, string>>({})
const isSubmitting = ref(false)
const imagePreview = ref<string | null>(props.project?.image || null)
const fileInput = ref<HTMLInputElement>()

// Constantes
const projectStatuses: ProjectStatus[] = ['PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SUSPENDED']

// Fonctions utilitaires
const getStatusLabel = (status: ProjectStatus): string => {
    const labels: Record<ProjectStatus, string> = {
        'PLANNED': 'Planifié',
        'IN_PROGRESS': 'En cours',
        'COMPLETED': 'Terminé',
        'SUSPENDED': 'Suspendu'
    }
    return labels[status]
}

const handleImageChange = (event: Event) => {
    const input = event.target as HTMLInputElement
    if (!input.files?.length) return

    const file = input.files[0]
    if (!file.type.startsWith('image/')) {
        errors.image = 'Le fichier doit être une image'
        return
    }

    form.image = file
    const reader = new FileReader()
    reader.onload = e => {
        imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
}

const removeImage = () => {
    form.image = null
    imagePreview.value = null
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

const triggerFileInput = () => {
    const input = fileInput.value
    if (input) {
        input.click()
    }
}

const validateForm = (): boolean => {
    errors.title = !form.title.trim() ? 'Le titre est requis' : ''
    errors.description = !form.description.trim() ? 'La description est requise' : ''

    if (form.start_date && form.end_date) {
        if (new Date(form.start_date) > new Date(form.end_date)) {
            errors.end_date = 'La date de fin doit être postérieure à la date de début'
        }
    }

    return !Object.values(errors).some(error => error)
}

const handleSubmit = async () => {
    if (!validateForm()) return

    isSubmitting.value = true
    const formData = new FormData()

    // Ajouter les champs au FormData
    Object.entries(form).forEach(([key, value]) => {
        if (value !== null && value !== '') {
            // Conversion explicite des valeurs pour FormData
            if (value instanceof File) {
                formData.append(key, value)
            } else if (typeof value === 'number') {
                formData.append(key, value.toString())
            } else {
                formData.append(key, value as string)
            }
        }
    })

    emit('submit', formData)
}
</script>
<template>
    <div class="project-card">
        <div class="project-image">
            <img :src="project.image || '/images/default-project.jpg'" :alt="project.title">
            <div class="project-status" :class="project.status.toLowerCase()">
                {{ getStatusLabel(project.status) }}
            </div>
        </div>

        <div class="project-content">
            <h3 class="project-title">{{ project.title }}</h3>

            <div class="project-info">
                <div class="info-item">
                    <Icon name="mdi:calendar" />
                    <span>{{ formatDate(project.start_date) }}</span>
                </div>
                <div class="info-item" v-if="project.budget">
                    <Icon name="mdi:currency-eur" />
                    <span>{{ formatBudget(project.budget) }} €</span>
                </div>
            </div>

            <p class="project-description">{{ truncateDescription(project.description) }}</p>

            <div class="project-footer">
                <div class="accountability-count">
                    <Icon name="mdi:comment-question" />
                    <span>{{ project.accountability_count }} demandes</span>
                </div>

                <button @click="openAccountabilityModal" class="accountability-btn">
                    Demander des comptes
                </button>
            </div>
        </div>

        <!-- Modal de demande de comptes -->
        <Modal v-model="showModal" title="Demander des comptes">
            <form @submit.prevent="submitAccountability" class="accountability-form">
                <div class="form-group">
                    <label for="question">Votre question ou demande :</label>
                    <textarea id="question" v-model="accountabilityForm.question" rows="4"
                        placeholder="Posez votre question concernant ce projet..." required></textarea>
                </div>

                <div class="form-actions">
                    <button type="button" @click="showModal = false" class="btn-cancel">
                        Annuler
                    </button>
                    <button type="submit" class="btn-submit" :disabled="isSubmitting">
                        <span v-if="isSubmitting">
                            <Icon name="mdi:loading" class="animate-spin" />
                            Envoi...
                        </span>
                        <span v-else>Envoyer la demande</span>
                    </button>
                </div>
            </form>
        </Modal>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Project, ProjectStatus } from '~/types'
import { useToast } from 'vue-toastification'

const toast = useToast()

const props = defineProps<{
    project: Project
}>()

const showModal = ref(false)
const isSubmitting = ref(false)
const accountabilityForm = ref({
    question: ''
})

const getStatusLabel = (status: ProjectStatus) => {
    const labels: Record<ProjectStatus, string> = {
        'PLANNED': 'Planifié',
        'IN_PROGRESS': 'En cours',
        'COMPLETED': 'Terminé',
        'SUSPENDED': 'Suspendu'
    }
    return labels[status]
}

const formatDate = (date: string | null) => {
    if (!date) return 'Date non définie'
    return new Date(date).toLocaleDateString('fr-FR')
}

const formatBudget = (budget: number) => {
    return new Intl.NumberFormat('fr-FR').format(budget)
}

const truncateDescription = (description: string, length = 150) => {
    if (description.length <= length) return description
    return description.substring(0, length) + '...'
}

const openAccountabilityModal = () => {
    showModal.value = true
}

const submitAccountability = async () => {
    try {
        isSubmitting.value = true

        const response = await fetch('http://localhost:8000/api/projects/accountability/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify({
                project: props.project.id,
                question: accountabilityForm.value.question
            })
        })

        if (!response.ok) {
            throw new Error('Erreur lors de l\'envoi de la demande')
        }

        toast.success('Votre demande a été envoyée avec succès')
        showModal.value = false
        accountabilityForm.value.question = ''

    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Une erreur est survenue lors de l\'envoi de votre demande')
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped>
.project-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease-in-out;
}

.project-card:hover {
    transform: translateY(-4px);
}

.project-image {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.project-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.project-status {
    position: absolute;
    top: 12px;
    right: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
    color: white;
}

.project-status.planned {
    background-color: #6366f1;
}

.project-status.in_progress {
    background-color: #0ea5e9;
}

.project-status.completed {
    background-color: #22c55e;
}

.project-status.suspended {
    background-color: #ef4444;
}

.project-content {
    padding: 1.5rem;
}

.project-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
}

.project-info {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
    font-size: 0.875rem;
}

.project-description {
    color: #4b5563;
    font-size: 0.875rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

.project-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}

.accountability-count {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
    font-size: 0.875rem;
}

.accountability-btn {
    background-color: #4f46e5;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 500;
    transition: background-color 0.2s;
}

.accountability-btn:hover {
    background-color: #4338ca;
}

.accountability-form {
    padding: 1rem;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    resize: vertical;
    min-height: 100px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}

.btn-cancel {
    padding: 0.5rem 1rem;
    border-radius: 6px;
    background-color: #f3f4f6;
    color: #4b5563;
    font-weight: 500;
}

.btn-submit {
    padding: 0.5rem 1rem;
    border-radius: 6px;
    background-color: #4f46e5;
    color: white;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-submit:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.animate-spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}
</style>
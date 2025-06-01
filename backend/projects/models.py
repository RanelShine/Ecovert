from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    """
    Modèle pour les projets environnementaux des communes
    """
    STATUS_CHOICES = [
        ('PLANNED', 'Planifié'),
        ('IN_PROGRESS', 'En cours'),
        ('COMPLETED', 'Terminé'),
        ('SUSPENDED', 'Suspendu'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Titre du projet"
    )
    description = models.TextField(
        verbose_name="Description détaillée"
    )
    commune = models.ForeignKey(
        'communes.Commune',
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="Commune"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED',
        verbose_name="État du projet"
    )
    start_date = models.DateField(
        verbose_name="Date de début",
        null=True,
        blank=True
    )
    end_date = models.DateField(
        verbose_name="Date de fin prévue",
        null=True,
        blank=True
    )
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Budget alloué",
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='projects/',
        verbose_name="Image du projet",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_projects',
        verbose_name="Créé par"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return f"{self.title} ({self.commune.nom})"

class Accountability(models.Model):
    """
    Modèle pour les demandes de comptes sur les projets
    """
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ANSWERED', 'Répondu'),
        ('CLOSED', 'Clôturé'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='accountability_requests',
        verbose_name="Projet concerné"
    )
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accountability_requests',
        verbose_name="Citoyen"
    )
    question = models.TextField(
        verbose_name="Question/Demande"
    )
    response = models.TextField(
        verbose_name="Réponse",
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="État de la demande"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de soumission"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='accountability_responses',
        verbose_name="Répondu par"
    )
    responded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de réponse"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Demande de compte"
        verbose_name_plural = "Demandes de comptes"

    def __str__(self):
        return f"Demande sur {self.project.title} par {self.citizen.username}"

    def save(self, *args, **kwargs):
        if self.response and not self.responded_at:
            self.responded_at = timezone.now()
            self.status = 'ANSWERED'
        super().save(*args, **kwargs) 
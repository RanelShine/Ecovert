from django.db import models
from accounts.models import User
from communes.models import Commune

class Signalement(models.Model):
    TYPE_SIGNALLEMENT_CHOICES = [
        ('dechets', 'Déchets'),
        ('pollution', 'Pollution'),
        ('climat', 'Climat'),
    ]

    objet = models.CharField(max_length=255)
    description = models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, default='En cours')
    localisation = models.CharField(max_length=255)
    type_signalement = models.CharField(max_length=50, choices=TYPE_SIGNALLEMENT_CHOICES)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.objet} - {self.type_signalement} ({self.statut})"

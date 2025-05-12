from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate
from django.apps import apps
from django.dispatch import receiver

class Commune(models.Model):
    nom = models.CharField(_('nom'), max_length=100)
    region = models.CharField(_('region'), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('commune')
        verbose_name_plural = _('communes')
        ordering = ['nom']
        
    def __str__(self):
        return self.nom

@receiver(post_migrate)
def create_default_communes(sender, **kwargs):
    if sender.label == 'communes':  # <-- nom exact de l'app dans INSTALLED_APPS
        Commune = apps.get_model('communes', 'Commune')
        default_communes = [
            {'id': 1, 'nom': 'Bafoussam I', 'region': 'Ouest'},
            {'id': 2, 'nom': 'Bafoussam II', 'region': 'Ouest'},
            {'id': 3, 'nom': 'Mandjou', 'region': 'Est'},
        ]
        for data in default_communes:
            Commune.objects.update_or_create(id=data['id'], defaults=data)

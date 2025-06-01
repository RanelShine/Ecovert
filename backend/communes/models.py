from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate
from django.apps import apps
from django.dispatch import receiver

class Commune(models.Model):
    nom = models.CharField(_('nom'), max_length=100)
    region = models.CharField(_('region'), max_length=100)
    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)
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
    if sender.label == 'communes':  
        Commune = apps.get_model('communes', 'Commune')
        default_communes = [
            {
                'id': 1,
                'nom': 'Bafoussam I',
                'region': 'Ouest',
                'latitude': 5.475,  # 5° 28′ 30″ N
                'longitude': 10.421  # 10° 25′ 15″ E
            },
            {
                'id': 2,
                'nom': 'Bafoussam II',
                'region': 'Ouest',
                'latitude': 5.516,  # 5° 30′ 59″ N
                'longitude': 10.410  # 10° 24′ 37″ E
            },
            {
                'id': 3,
                'nom': 'Mandjou',
                'region': 'Est',
                'latitude': 4.600,  # 4° 36′ N
                'longitude': 13.733  # 13° 44′ E
            },
        ]
        for data in default_communes:
            Commune.objects.update_or_create(id=data['id'], defaults=data)

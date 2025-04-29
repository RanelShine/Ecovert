from django.db import models
from django.utils.translation import gettext_lazy as _

class Commune(models.Model):
    nom = models.CharField(_('nom'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('commune')
        verbose_name_plural = _('communes')
        ordering = ['nom']
        
    def __str__(self):
        return self.nom
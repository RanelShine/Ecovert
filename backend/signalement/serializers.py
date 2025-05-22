from rest_framework import serializers
from .models import Signalement

class SignalementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signalement
        fields = ['id', 'objet', 'description', 'date_signalement', 'date_resolution', 'statut', 'localisation', 'type_signalement', 'utilisateur_id', 'photo_id']
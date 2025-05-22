from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from photos.models import Photo
from .models import Signalement

permission_classes = [IsAuthenticated]
authentication_classes = [JWTAuthentication]

import traceback

@api_view(['POST'])
def create_signalement(request):
    data = request.data
    print("Authentifié ?", request.user)
    print("Photo ID reçu :", data.get('photo_id'))
    print("Données reçues :", request.data)
    utilisateur = request.user
    if not utilisateur.is_authenticated:
        return Response({'error': 'Utilisateur non authentifié'}, status=401)

    try:
        photo_id = data.get('photo_id')
        photo_instance = None
        if photo_id:
            try:
                photo_instance = Photo.objects.get(id=photo_id)
            except Photo.DoesNotExist:
                return Response({'error': 'Photo non trouvée'}, status=400)

        signalement = Signalement.objects.create(
            objet=data['objet'],
            description=data['description'],
            localisation=data['localisation'],
            type_signalement=data['type_signalement'],
            utilisateur=utilisateur,
            photo_id=photo_instance.id,
        )
        return Response({'message': 'Signalement créé avec succès'}, status=201)

    except Exception as e:
        traceback.print_exc()  # Affiche la trace complète dans la console serveur
        return Response({'error': str(e)}, status=400)



# Liste des signalements
def list_signalements(request):
    if request.method == 'GET':
        signalements = Signalement.objects.all().values()
        return JsonResponse(list(signalements), safe=False)

# Détails d'un signalement
def detail_signalement(request, id):
    try:
        signalement = Signalement.objects.get(pk=id)
        return JsonResponse({
            "id": signalement.id,
            "objet": signalement.objet,
            "description": signalement.description,
            "date_signalement": signalement.date_signalement,
            "date_resolution": signalement.date_resolution,
            "statut": signalement.statut,
            "localisation": signalement.localisation,
            "type_signalement": signalement.type_signalement,
            "utilisateur_id": signalement.utilisateur_id,
            "commune_id": signalement.commune_id
        })
    except Signalement.DoesNotExist:
        return JsonResponse({"error": "Signalement non trouvé"}, status=404)


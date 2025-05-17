from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Photo
from .serializers import PhotoSerializer

# POST : Envoie une photo avec lat/lon
class UploadPhotoView(APIView):
    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Photo enregistrée avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET : Liste toutes les photos avec leurs coordonnées
def photo_locations(request):
    data = [
        {
            'id': photo.id,
            'image_url': request.build_absolute_uri(photo.image.url),
            'latitude': photo.latitude,
            'longitude': photo.longitude,
            'date_uploaded': photo.date_uploaded.strftime('%Y-%m-%d %H:%M:%S')
        }
        for photo in Photo.objects.all()
    ]
    return JsonResponse(data, safe=False)
class PhotoLocationView(APIView):
    def get(self, request):
        data = [
            {
                'id': photo.id,
                'image_url': request.build_absolute_uri(photo.image.url),
                'latitude': photo.latitude,
                'longitude': photo.longitude,
                'date_uploaded': photo.date_uploaded.strftime('%Y-%m-%d %H:%M:%S')
            }
            for photo in Photo.objects.all()
        ]
        return Response(data, status=status.HTTP_200_OK)
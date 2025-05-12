from rest_framework import viewsets
from .models import Commune
from .serializers import CommuneSerializer

class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer

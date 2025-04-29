from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Commune
from .serializers import CommuneSerializer

class CommuneViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for read-only Commune operations."""
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [AllowAny]
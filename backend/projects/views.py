from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Project, Accountability
from .serializers import (
    ProjectListSerializer, ProjectDetailSerializer,
    AccountabilitySerializer, AccountabilityCreateSerializer,
    AccountabilityResponseSerializer
)

class IsCTDOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre uniquement aux CTD de créer/modifier des projets
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ctd'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'cdt'

# Project views
@api_view(['GET'])
def list_projects(request):
    """Liste tous les projets avec filtres optionnels"""
    queryset = Project.objects.select_related('commune', 'created_by')
    
    # Filtrer par commune si spécifié
    commune_id = request.query_params.get('commune')
    if commune_id:
        queryset = queryset.filter(commune_id=commune_id)
    
    # Filtrer par statut si spécifié
    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(status=status_param)
    
    # Recherche par titre ou description
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    queryset = queryset.order_by('-created_at')
    serializer = ProjectListSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsCTDOrReadOnly])
def create_project(request):
    """Crée un nouveau projet"""
    serializer = ProjectListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            created_by=request.user,
            commune=request.user.commune
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def project_detail(request, id):
    """Récupère les détails d'un projet spécifique"""
    try:
        project = Project.objects.get(pk=id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    except Project.DoesNotExist:
        return Response(
            {'error': 'Projet non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsCTDOrReadOnly])
def update_project(request, id):
    """Met à jour un projet existant"""
    try:
        project = Project.objects.get(pk=id)
        
        # Vérifier que l'utilisateur est un CTD de la bonne commune
        if request.user.role != 'ctd' or request.user.commune != project.commune:
            return Response(
                {'error': 'Vous n\'êtes pas autorisé à modifier ce projet'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ProjectDetailSerializer(
            project,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return Response(
            {'error': 'Projet non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsCTDOrReadOnly])
def delete_project(request, id):
    """Supprime un projet"""
    try:
        project = Project.objects.get(pk=id)
        
        # Vérifier que l'utilisateur est un CTD de la bonne commune
        if request.user.role != 'ctd' or request.user.commune != project.commune:
            return Response(
                {'error': 'Vous n\'êtes pas autorisé à supprimer ce projet'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Project.DoesNotExist:
        return Response(
            {'error': 'Projet non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )

# Accountability views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_accountability(request):
    """Liste les demandes de comptes selon le rôle de l'utilisateur"""
    user = request.user
    
    # Les CTD voient toutes les demandes de leur commune
    if user.role == 'ctd':
        queryset = Accountability.objects.filter(
            project__commune=user.commune
        ).select_related('project', 'citizen', 'responded_by')
    # Les citoyens ne voient que leurs propres demandes
    else:
        queryset = Accountability.objects.filter(
            citizen=user
        ).select_related('project', 'citizen', 'responded_by')
    
    serializer = AccountabilitySerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_accountability(request):
    """Crée une nouvelle demande de comptes"""
    serializer = AccountabilityCreateSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def accountability_detail(request, id):
    """Récupère les détails d'une demande de comptes"""
    try:
        accountability = Accountability.objects.get(pk=id)
        
        # Vérifier les permissions
        if request.user.role == 'ctd':
            if request.user.commune != accountability.project.commune:
                return Response(
                    {'error': 'Vous n\'êtes pas autorisé à voir cette demande'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif accountability.citizen != request.user:
            return Response(
                {'error': 'Vous n\'êtes pas autorisé à voir cette demande'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AccountabilitySerializer(accountability)
        return Response(serializer.data)
    except Accountability.DoesNotExist:
        return Response(
            {'error': 'Demande non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsCTDOrReadOnly])
def respond_accountability(request, id):
    """Répond à une demande de comptes"""
    try:
        accountability = Accountability.objects.get(pk=id)
        
        # Vérifier que l'utilisateur est un CTD de la bonne commune
        if request.user.role != 'ctd' or request.user.commune != accountability.project.commune:
            return Response(
                {'error': 'Vous n\'êtes pas autorisé à répondre à cette demande'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AccountabilityResponseSerializer(
            accountability,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(AccountabilitySerializer(accountability).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Accountability.DoesNotExist:
        return Response(
            {'error': 'Demande non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        ) 
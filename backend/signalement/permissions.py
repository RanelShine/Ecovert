#signalement/permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement aux administrateurs de modifier les objets.
    Les autres utilisateurs peuvent seulement lire.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement aux propriétaires d'un objet de le modifier.
    """
    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Permissions d'écriture seulement pour le propriétaire
        return (request.user.is_authenticated and 
                hasattr(obj, 'utilisateur') and 
                obj.utilisateur == request.user)


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission personnalisée qui permet aux administrateurs et aux propriétaires de modifier les objets.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (request.user.is_authenticated and 
                (request.user.role == 'admin' or 
                 (hasattr(obj, 'utilisateur') and obj.utilisateur == request.user)))


class IsCtdOrAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour les ctd et administrateurs.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['ctd', 'admin'])


class IsAdminOnly(permissions.BasePermission):
    """
    Permission réservée aux administrateurs uniquement.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role == 'admin')


class IsCitoyenOrAdmin(permissions.BasePermission):
    """
    Permission pour les citoyens et administrateurs.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['citoyen', 'admin'])


class CanCreateSignalement(permissions.BasePermission):
    """
    Permission pour créer des signalements.
    Seuls les citoyens authentifiés peuvent créer des signalements.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return (request.user.is_authenticated and 
                    request.user.role == 'citoyen')
        return True


class CanManageSignalement(permissions.BasePermission):
    """
    Permission complexe pour la gestion des signalements selon les rôles.
    """
    def has_permission(self, request, view):
        # Autoriser l'accès général aux utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Pour les opérations de création/modification, vérifier l'authentification
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                # Utilisateurs non authentifiés : seulement signalements publics
                return hasattr(obj, 'statut') and obj.statut in ['en_cours', 'en_attente', 'traite', 'rejeté', 'suspendu']
            
            elif request.user.role == 'citoyen':
                # Citoyens : seulement leurs signalements ou signalements publics
                return (obj.utilisateur == request.user or
                       (hasattr(obj, 'statut') and obj.statut in ['en_cours', 'en_attente', 'traite', 'rejeté', 'suspendu']))

            elif request.user.role == 'ctd':
                # CTD : signalements de leur commune
                return (hasattr(request.user, 'commune') and
                        request.user.commune and
                        hasattr(obj, 'commune') and
                        obj.commune == request.user.commune)
            
            elif request.user.role == 'admin':
                # Administrateurs : tous les signalements
                return True
        
        # Permissions d'écriture/suppression
        if not request.user.is_authenticated:
            return False
            
        if request.user.role == 'citoyen':
            # Citoyens : seulement leurs signalements et seulement modification limitée
            return (obj.utilisateur == request.user and 
                   hasattr(obj, 'statut') and 
                   obj.statut in ['en_cours', 'en_attente', 'traite', 'rejeté', 'suspendu'])
        
        elif request.user.role == 'ctd':
            #ctd : signalements de leur commune
            return (hasattr(request.user, 'commune') and 
                    request.user.commune and 
                    hasattr(obj, 'commune') and
                    obj.commune == request.user.commune)
        
        elif request.user.role == 'admin':
            # Administrateurs : tous les signalements
            return True
        
        return False


class CanUpdateSignalementStatus(permissions.BasePermission):
    """
    Permission pour modifier le statut des signalements.
    Réservée aux ctd et administrateurs.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['ctd', 'admin'])

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
            
        if request.user.role == 'admin':
            return True

        if request.user.role == 'ctd':
            # CTD : seulement signalements de leur commune
            return (hasattr(request.user, 'commune') and
                    request.user.commune and
                    hasattr(obj, 'commune') and
                    obj.commune == request.user.commune)
        
        return False


class CanViewSignalement(permissions.BasePermission):
    """
    Permission pour visualiser les signalements selon le rôle.
    """
    def has_permission(self, request, view):
        return True  # Autoriser l'accès général

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            # Utilisateurs non authentifiés : seulement signalements publics
            return hasattr(obj, 'statut') and obj.statut in ['en_cours', 'en_attente', 'traite', 'rejeté', 'suspendu']
        
        if request.user.role == 'citoyen':
            # Citoyens : tous leurs signalements
            return obj.utilisateur == request.user
        
        elif request.user.role == 'ctd':
            # CTD : signalements de leur commune
            return (hasattr(request.user, 'commune') and
                    request.user.commune and
                    hasattr(obj, 'commune') and
                    obj.commune == request.user.commune)
        
        elif request.user.role == 'admin':
            # Administrateurs : tous les signalements
            return True
        
        return False


class CanManageComments(permissions.BasePermission):
    """
    Permission pour gérer les commentaires sur les signalements.
    """
    def has_permission(self, request, view):
        # Lecture autorisée pour tous, écriture pour utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture/suppression
        if not request.user.is_authenticated:
            return False
            
        # Propriétaire du commentaire
        if hasattr(obj, 'auteur') and obj.auteur == request.user:
            return True
            
        # Administrateurs peuvent tout gérer
        if request.user.role == 'admin':
            return True
            
        # CTD peuvent gérer les commentaires dans leur commune
        if request.user.role == 'ctd':
            return (hasattr(request.user, 'commune') and 
                    request.user.commune and 
                    hasattr(obj, 'signalement') and
                    hasattr(obj.signalement, 'commune') and
                    obj.signalement.commune == request.user.commune)
        
        return False


class CanAccessStatistics(permissions.BasePermission):
    """
    Permission pour accéder aux statistiques.
    Réservée auxctd et administrateurs.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['ctd', 'admin'])


class CanManageUsers(permissions.BasePermission):
    """
    Permission pour gérer les utilisateurs.
    Réservée aux administrateurs uniquement.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and 
                request.user.role == 'admin')


class IsProfileOwnerOrAdmin(permissions.BasePermission):
    """
    Permission pour gérer les profils utilisateurs.
    Propriétaire ou administrateur seulement.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (request.user == obj or 
                request.user.role == 'admin')


# Permissions composées pour des cas d'usage spécifiques
class SignalementViewPermission(permissions.BasePermission):
    """
    Permission composite pour les vues de signalement.
    Combine plusieurs logiques selon l'action.
    """
    def has_permission(self, request, view):
        # Autoriser l'accès général
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Création : seulement citoyens
        if view.action == 'create':
            return (request.user.is_authenticated and 
                    request.user.role == 'citoyen')
        
        # Autres actions : utilisateurs authentifiés
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Déléguer à CanManageSignalement pour la logique complexe
        can_manage = CanManageSignalement()
        return can_manage.has_object_permission(request, view, obj)
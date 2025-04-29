import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, VerifyEmailSerializer

def generate_verification_code(length=6):
    """Generate a random verification code."""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(user):
    """Send verification email to user."""
    code = generate_verification_code()
    user.verification_code = code
    user.save()
    
    subject = 'Confirmation de votre inscription - Redevabilité Verte'
    message = f'''Bonjour {user.prenom},
    
Merci de vous être inscrit sur la plateforme Redevabilité Verte.
Pour confirmer votre adresse email, veuillez utiliser le code suivant : {code}

À bientôt sur notre plateforme !
L'équipe Redevabilité Verte
'''
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    return code

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Send verification email
        send_verification_email(user)
        return Response({
            'message': 'Inscription réussie ! Veuillez vérifier votre email pour activer votre compte.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Verify user email with verification code."""
    serializer = VerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['verification_code']
        
        try:
            user = User.objects.get(email=email, verification_code=code)
            user.is_verified = True
            user.is_active = True
            user.verification_code = None
            user.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Email vérifié avec succès !',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'Code de vérification invalide.'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Log in a user."""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            if not user.is_verified:
                return Response({
                    'error': 'Veuillez vérifier votre email avant de vous connecter.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Connexion réussie !',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Email ou mot de passe invalide.'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Log out a user."""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Déconnexion réussie !"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Erreur lors de la déconnexion"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User CRUD operations."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
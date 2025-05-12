from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserRegisterSerializer, LoginSerializer
import random
import string

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Générer un code de vérification (6 chiffres)
            verification_code = ''.join(random.choices(string.digits, k=6))
            
            # Enregistrer l'utilisateur
            user = serializer.save(verification_code=verification_code, is_active=False)
            
            # send_verification_email(user.email, verification_code)
            
            return Response({
                'success': True,
                'message': 'Compte créé avec succès. Veuillez vérifier votre email pour activer votre compte.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        try:
            user = User.objects.get(email=email, verification_code=code)
            user.is_active = True
            user.is_verified = True
            user.verification_code = None
            user.save()
            
            return Response({
                'success': True,
                'message': 'Compte activé avec succès.'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Code de vérification invalide ou utilisateur introuvable.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Crée un refresh et access token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'user': UserSerializer(user).data,
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

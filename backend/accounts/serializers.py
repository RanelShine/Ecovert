from rest_framework import serializers
from .models import User
from communes.models import Commune
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ['id', 'nom']

class UserSerializer(serializers.ModelSerializer):
    commune = CommuneSerializer(read_only=True)
    commune_id = serializers.PrimaryKeyRelatedField(
        queryset=Commune.objects.all(),
        source='commune',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'prenom', 'telephone', 'role', 'commune', 'commune_id', 'is_verified']
        read_only_fields = ['is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    commune_id = serializers.PrimaryKeyRelatedField(
        queryset=Commune.objects.all(),
        source='commune',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'prenom', 'telephone', 'password', 'password_confirm', 'role', 'commune_id']
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Les mots de passe ne correspondent pas.'})
        
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e)})
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            telephone=validated_data.get('telephone', ''),
            role=validated_data['role'],
            commune=validated_data.get('commune', None)
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(required=True, max_length=6)
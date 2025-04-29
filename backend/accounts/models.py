from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from communes.models import Commune

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse email est obligatoire'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Administrateur')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Citoyens', 'Citoyens'),
        ('ONG', 'ONG'),
        ('Entreprise', 'Entreprise'),
        ('Administrateur', 'Administrateur'),
    )
    
    email = models.EmailField(_('adresse email'), unique=True)
    nom = models.CharField(_('nom'), max_length=150)
    prenom = models.CharField(_('prénom'), max_length=150)
    telephone = models.CharField(_('téléphone'), max_length=15, blank=True)
    role = models.CharField(_('rôle'), max_length=15, choices=ROLE_CHOICES, default='Citoyens')
    commune = models.ForeignKey('communes.Commune', on_delete=models.SET_NULL, null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role']
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email})"
        
    def get_full_name(self):
        return f"{self.nom} {self.prenom}"
    
    def get_short_name(self):
        return self.nom
# backend/accounts/urls.py
from django.urls import path
from .views import RegisterView, VerifyAccountView, LoginView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyAccountView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
]
from django.urls import path
from .views import RegisterView, VerifyAccountView, LoginView
from .views import CurrentUserAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyAccountView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
]
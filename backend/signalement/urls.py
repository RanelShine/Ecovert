from django.urls import path
from . import views

urlpatterns = [
    path('liste/', views.list_signalements, name='list-signalements'),
    path('detail/<int:id>/', views.detail_signalement, name='detail-signalement'),
    path('create/', views.create_signalement, name='create-signalement'),
]

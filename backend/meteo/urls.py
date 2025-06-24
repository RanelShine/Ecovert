from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.global_weather),
    path('weather/position/', views.weather_by_position),
]

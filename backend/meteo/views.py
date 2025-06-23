import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

API_KEY = "CLÉ_API_OPENWEATHER"

@api_view(['GET'])
def global_weather(request):
    # Coordonnées par défaut (ex : Yaoundé)
    lat = 3.848
    lon = 11.5021
    return get_weather_data(lat, lon)

@api_view(['GET'])
def weather_by_position(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    if not lat or not lon:
        return Response({"error": "Coordonnées manquantes"}, status=400)
    return get_weather_data(lat, lon)

def get_weather_data(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&lang=fr&appid={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    return Response(data)



import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def get_weather(request):
    # Replace with your actual OpenWeatherMap API key
    api_key = "0b2b39a7d39e5b4e175aa06179ac86b2"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            # Remove extra city entries until only less than 2 remain
            while City.objects.count() >= 2:
                # Order by ID (oldest first) and delete the first city
                City.objects.order_by('id').first().delete()
            form.save()

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city.name, api_key)).json()
        print(response)  # Debug: prints API response to console

        if response.get("main"):
            weather = {
                "city": city.name,
                "temperature": response["main"]["temp"],
                "description": response["weather"][0]["description"],
                "icon": response["weather"][0]["icon"],
            }
            weather_data.append(weather)
        else:
            weather_data.append({
                "city": city.name,
                "temperature": "N/A",
                "description": response.get("message", "Error fetching data"),
                "icon": "",
            })

    return render(request, "weather/weather.html", {"weather_data": weather_data, "form": form})

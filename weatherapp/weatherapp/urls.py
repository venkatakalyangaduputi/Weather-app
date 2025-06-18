from django.contrib import admin
from django.urls import path
from weather.views import get_weather

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_weather, name='weather-home'),
]

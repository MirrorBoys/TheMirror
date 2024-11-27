from django.urls import path
from . import views

urlpatterns = [
    path("fetch/<int:numberOfDays>", views.fetchWeather, name="apiWeatherFetch"),
]

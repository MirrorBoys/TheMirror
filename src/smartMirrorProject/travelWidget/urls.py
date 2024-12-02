from django.urls import path
from . import views

urlpatterns = [
    path("fetch/journeys/<str:start_station>/<str:end_station>/<int:amount_trips>", views.fetch_trip, name="apiFetchTrip"),
    path("fetch/departures/<str:station>/<str:destination_filter>/", views.fetch_departures, name="apiFetchDepartures"),
    path("fetch/departures/<str:station>/", views.fetch_departures, name="apiFetchDepartures"),
]

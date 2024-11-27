from django.urls import path
from . import views

urlpatterns = [
    path("fetch/<str:start_station>/<str:end_station>/<int:amount_trips>", views.fetch_trip, name="apiTravelFetch"),
]

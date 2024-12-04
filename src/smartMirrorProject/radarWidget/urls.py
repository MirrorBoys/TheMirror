from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Example URL pattern.
    path("fetch/coordinates/<str:placename>/", views.fetch_coordinates, name="fetch_coordinates"),

    # Breakdown of the route:
    # - fetch: indicates that the URL is used to fetch data.
    # - <str:start_station>: a parameter of datatype string is passed to the API.
    # - <str:end_station>: a parameter of datatype string is passed to the API.
    # - and so on.

    # Add your URL pattern here
]
from django.urls import path
from . import views

urlpatterns = [
    path(
        "fetch/<str:apiKey>/<str:origin>/<str:destination>/<str:mode>/",
        views.createMapsData,
        name="apiMapsFetch",
    ),
]

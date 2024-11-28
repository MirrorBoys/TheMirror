from django.urls import path
from . import views

urlpatterns = [
    path("fetch/", views.fetch_agenda_events_view, name="fetch-agenda-events"),
]

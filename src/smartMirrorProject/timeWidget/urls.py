from django.urls import path
from . import views

urlpatterns = [
    path("fetch/<str:timezone>", views.current_time, name="current_time"),
    path("fetch-timezone", views.fetch_timezone, name="fetch_timezone"),
]

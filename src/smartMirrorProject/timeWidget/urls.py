from django.urls import path
from . import views

urlpatterns = [
    path("fetch/<str:timezone>", views.current_time, name="current_time"),
]

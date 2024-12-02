from django.urls import path
from . import views

urlpatterns = [
    path("fetch/<str:timezone>", views.current_time, name="current_time"),
    path("fetch-session-timezone/", views.fetch_session_timezone, name="get_session_timezone"),	
]

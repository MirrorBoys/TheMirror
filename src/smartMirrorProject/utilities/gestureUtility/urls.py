from django.urls import path
from . import views


urlpatterns = [
    path('fetch/', views.sendGestureData, name='sendGestureData'),
]
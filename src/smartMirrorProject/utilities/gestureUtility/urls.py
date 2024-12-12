from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.math, name='math'),
]
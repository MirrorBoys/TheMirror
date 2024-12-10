from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.fetch_notes, name='fetch_notes')
]

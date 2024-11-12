from django.urls import path
from . import views

urlpatterns = [
    path('grid/', views.grid, name='grid'),
]

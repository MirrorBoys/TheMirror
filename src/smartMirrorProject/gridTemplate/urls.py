from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('grid/', views.grid, name='grid'),
    path('', views.widget, name='widget'),
]
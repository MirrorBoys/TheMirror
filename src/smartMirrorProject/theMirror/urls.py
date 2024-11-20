from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('get-playlist/', views.get_playlist, name='get_playlist'),
    path('refresh-token/', views.refresh_token, name='refresh_token'),
]

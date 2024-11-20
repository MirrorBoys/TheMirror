from django.urls import path

from . import views
from . import spotify

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', spotify.login, name='login'),
    path('callback/', spotify.callback, name='callback'),
    path('get-playlist/', spotify.get_playlist, name='get_playlist'),
    path('refresh-token/', spotify.refresh_token, name='refresh_token'),
]

from django.urls import path

from . import views
from . import spotify

urlpatterns = [
    path("", views.index, name="index"),
    path('spotify-login/', spotify.spotify_login, name='login'),
    path('spotify-callback/', spotify.spotify_callback, name='callback'),
    path('spotify-logout/', spotify.spotify_logout, name='logout'),
    path('spotify-get-playlist/', spotify.spotify_get_playlist, name='get_playlist'),
    path('spotify-refresh-token/', spotify.spotify_refresh_token, name='refresh_token'),
    path('spotify-add-song/', spotify.spotify_add_song_to_queue, name='add_song'),
]

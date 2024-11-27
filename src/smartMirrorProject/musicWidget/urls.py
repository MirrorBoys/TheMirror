from django.urls import path
from . import views

urlpatterns = [
    path("spotify-login/",views.spotify_login, name="spotify-login"),
    path('spotify-callback/', views.spotify_callback, name='spotify-callback'),
    path('spotify-logout/', views.spotify_logout, name='spotify-logout'),
    path('spotify-get-playlist/', views.spotify_get_playlist, name='spotify-get-playlist'),
    path('spotify-refresh-token/', views.spotify_refresh_token, name='spotify-refresh-token'),
    path('spotify-add-song/', views.spotify_add_song_to_queue, name='spotify-add-song'),
]
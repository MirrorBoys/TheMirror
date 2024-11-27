import os
from datetime import datetime
import requests
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

# from dotenv import load_dotenv

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

REDIRECT_URI='http://127.0.0.1:8000/musicWidget/spotify-callback'
AUTH_URL='https://accounts.spotify.com/authorize'
TOKEN_URL='https://accounts.spotify.com/api/token'
API_BASE_URL='https://api.spotify.com/v1/'

def spotify_login(request):
    scope = 'user-read-private user-read-email streaming'
    
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&scope={scope}&redirect_uri={REDIRECT_URI}&show_dialog=True"
    return redirect(auth_url)

def spotify_logout(request):
    request.session.flush()
    return redirect('/')

def spotify_callback(request):
    if 'error' in request.GET:
        return HttpResponse(request.GET['error'])
    
    if 'code' in request.GET:
        req_body = {
            'code': request.GET['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        request.session['access_token'] = token_info['access_token']
        request.session['refresh_token'] = token_info['refresh_token']
        request.session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/')
    
def spotify_get_playlist(request):
    if 'access_token' not in request.session:
        return redirect('/spotify-login')
    
    if datetime.now().timestamp() > request.session['expires_at']:
        print('Token expired. Refreshing token...')
        spotify_refresh_token(request)
    
    headers = {
        'Authorization': f"Bearer {request.session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    
    playlist_data = [{"name": playlist["name"], "url": playlist["external_urls"]["spotify"]} for playlist in playlists["items"]]
    
    return playlist_data

def spotify_refresh_token(request):
    if 'refresh_token' not in request.session:
        return redirect('/spotify-login')
    
    if datetime.now().timestamp() > request.session['expires_at']:
        print('Token expired. Refreshing token...')
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': request.session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        
        request.session['access_token'] = new_token_info['access_token']
        request.session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
        return redirect('/')
    
    # If the token is not expired, redirect to the playlist page
    return redirect('/')

def spotify_add_song_to_queue(request):
    if 'access_token' not in request.session:
        return JsonResponse({"error": "User not logged in"}, status=401)

    if datetime.now().timestamp() > request.session['expires_at']:
        spotify_refresh_token(request)

    song_uri = request.GET.get('track_uri')
    if not song_uri:
        return JsonResponse({"error": "No song URI provided"}, status=400)

    headers = {
        'Authorization': f"Bearer {request.session['access_token']}"
    }

    response = requests.post(f"{API_BASE_URL}me/player/queue?uri={song_uri}", headers=headers)

    if response.status_code == 200:
        return JsonResponse({"message": "Song added to queue"}, status=200)
    else:
        return JsonResponse({"error": "Failed to add song to queue"}, status=response.status_code)
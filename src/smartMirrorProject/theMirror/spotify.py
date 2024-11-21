import urllib.parse
import requests
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse

import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
API_BASE_URL = os.getenv('API_BASE_URL')

def login(request):
    scope = 'user-read-private user-read-email streaming'
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': False
    }
    
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

def callback(request):
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
        request.session['expires_at'] = datetime.now().timestamp() + 1
        
        return redirect('/theMirror')
    
def get_playlist(request):
    if 'access_token' not in request.session:
        return redirect('/login')
    
    if datetime.now().timestamp() > request.session['expires_at']:
        print('Token expired. Refreshing token...')
        refresh_token(request)
    
    headers = {
        'Authorization': f"Bearer {request.session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    
    playlist_data = [{"name": playlist["name"], "url": playlist["external_urls"]["spotify"]} for playlist in playlists["items"]]
    
    return playlist_data

def refresh_token(request):
    if 'refresh_token' not in request.session:
        return redirect('/login')
    
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
        request.session['expires_at'] = datetime.now().timestamp() + 1
        
        return redirect('/theMirror')
    
    # If the token is not expired, redirect to the playlist page
    return redirect('/theMirror')
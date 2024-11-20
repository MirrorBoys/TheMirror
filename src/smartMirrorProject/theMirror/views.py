import feedparser
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import urllib.parse
from datetime import datetime
from django.http import JsonResponse
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
    scope = 'user-read-private user-read-email'
    
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
        request.session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
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
        request.session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
        return redirect('/theMirror')
    
    # If the token is not expired, redirect to the playlist page
    return redirect('/theMirror')

def fetch_news():
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    news_data = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:2]]
    return news_data

def time_api(request):
    response = requests.get(
        "https://www.timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam",
        timeout=10,
    )
    data = response.json()
    time_data = {
        "time": data["time"],
        "seconds": data["seconds"],
        "date": data["date"],
        "dayOfWeek": data["dayOfWeek"],
    }
    return time_data

def index(request):
    # Example data with widget types or specific templates
    widgets = {
        "Weather_1": {
            "id": 1,
            "type": "weather",
            "data": {"temperature": 22, "condition": "Sunny"},
        },
        "Weather_2": {
            "id": 2,
            "type": "weather",
            "data": {"temperature": 18, "condition": "Cloudy"},
        },
        "Weather_3": {
            "id": 3,
            "type": "weather",
            "data": {"temperature": 25, "condition": "Rainy"},
        },
        "Weather_4": {
            "id": 4,
            "type": "weather",
            "data": {"temperature": 30, "condition": "Sunny"},
        },
        "Weather_5": {
            "id": 5,
            "type": "weather",
            "data": {"temperature": 20, "condition": "Windy"},
        },
        "Weather_6": {
            "id": 6,
            "type": "weather",
            "data": {"temperature": 17, "condition": "Snowy"},
        },
        "Weather_7": {
            "id": 7,
            "type": "weather",
            "data": {"temperature": 24, "condition": "Cloudy"},
        },
        "Weather_8": {
            "id": 8,
            "type": "weather",
            "data": {"temperature": 27, "condition": "Sunny"},
        },
        "Weather_9": {
            "id": 9,
            "type": "weather",
            "data": {"temperature": 19, "condition": "Rainy"},
        },
        "Weather_10": {
            "id": 10,
            "type": "weather",
            "data": {"temperature": 21, "condition": "Windy"},
        },
        "Weather_11": {
            "id": 11,
            "type": "weather",
            "data": {"temperature": 23, "condition": "Sunny"},
        },
        "Weather_12": {
            "id": 12,
            "type": "weather",
            "data": {"temperature": 26, "condition": "Cloudy"},
        },
        "Weather_13": {
            "id": 13,
            "type": "weather",
            "data": {"temperature": 22, "condition": "Rainy"},
        },
        "Weather_14": {
            "id": 14,
            "type": "weather",
            "data": {"temperature": 29, "condition": "Sunny"},
        },
        "Weather_15": {
            "id": 15,
            "type": "weather",
            "data": {"temperature": 28, "condition": "Windy"},
        },
        "Weather_16": {
            "id": 16,
            "type": "weather",
            "data": {"temperature": 20, "condition": "Snowy"},
        },
        "Weather_17": {
            "id": 17,
            "type": "weather",
            "data": {"temperature": 18, "condition": "Cloudy"},
        },
        "Weather_18": {
            "id": 18,
            "type": "weather",
            "data": {"temperature": 25, "condition": "Rainy"},
        },
        "Weather_19": {
            "id": 19,
            "type": "weather",
            "data": {"temperature": 21, "condition": "Windy"},
        },
        "Time": {
            "id": 21,
            "type": "time",
            "data": time_api(request)
        },          
        "News": {
            "id": 22,
            "type": "news",
            "data": fetch_news()
        },
        "Music": {
            "id": 23,
            "type": "music",
            "data": get_playlist(request) if request.user.is_authenticated else None,
        },
    }
    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)
import feedparser
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import spotipy
from spotipy import SpotifyOAuth

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

def fetch_current_song(request):
    token = request.session.get("spotify_token")
    if not token:
        return {"song": "Not logged in", "artist": "N/A"}

    sp = spotipy.Spotify(auth=token)
    current_track = sp.current_playback()
    if not current_track or not current_track['is_playing']:
        return {"song": "No song playing", "artist": "N/A"}

    item = current_track['item']
    return {
        "song": item['name'],
        "artist": ", ".join([artist['name'] for artist in item['artists']])
    }
    
def exchange_code_for_token(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("No code provided", status=400)

    try:
        token_info = sp_oauth.get_access_token(code)
        request.session["spotify_token"] = token_info["access_token"]
        return HttpResponse("Token successfully retrieved and stored in session")
    except Exception as e:
        return HttpResponse(f"Error retrieving token: {str(e)}", status=500)

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
        "News": {
            "id": 22,
            "type": "news",
            "data": fetch_news()
        },
        "Time": {
            "type": "time",
            "data": time_api(request)
        },
        "Music": {
            "id": 23,
            "type": "music",
            "data": fetch_current_song(request)
        },
    }
    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

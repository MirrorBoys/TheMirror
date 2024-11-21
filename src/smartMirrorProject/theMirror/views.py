import feedparser
from django.http import HttpResponse
from django.shortcuts import render
import requests
import time
import datetime


def fetch_news():
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    news_data = [
        {"title": entry.title, "link": entry.link} for entry in feed.entries[:2]
    ]
    return news_data


cached_time_data = {}
last_fetched_time = 0


def time_api(request):
    global cached_time_data
    global last_fetched_time
    elapsed_seconds = int(time.time() - last_fetched_time)
    if not cached_time_data or (time.time() - last_fetched_time) > 3600:  # 1 hour
        response = requests.get(
            "https://www.timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam",
            timeout=10,
        )
        data = response.json()
        cached_time_data = {
            "hour": data["hour"],
            "minute": data["minute"],
            "seconds": data["seconds"],
            "date": data["date"],
            "dayOfWeek": data["dayOfWeek"],
        }
        last_fetched_time = time.time()
    else:
        cached_time_data["seconds"] += 1
        if cached_time_data["seconds"] >= 59:
            cached_time_data["seconds"] = 0
            cached_time_data["minute"] += 1
        if cached_time_data["minute"] >= 59:
            cached_time_data["minute"] = 0
            cached_time_data["hour"] += 1
        if cached_time_data["hour"] >= 23:
            cached_time_data["hour"] = 0

    return cached_time_data


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
            "data": {"temperature": 24, "condition": "Sunny"},
        },
        "Weather_20": {
            "id": 20,
            "type": "weather",
            "data": {"temperature": 21, "condition": "Windy"},
        },
        "News": {"id": 22, "type": "news", "data": fetch_news()},
        "Time": {"type": "time", "data": time_api(request)},
    }

    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

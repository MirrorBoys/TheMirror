import feedparser
from django.http import HttpResponse
from django.shortcuts import render
import requests


def fetch_news():
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    news_data = [
        {"title": entry.title, "link": entry.link} for entry in feed.entries[:2]
    ]
    return news_data


def index(request):
    # Example data with widget types or specific templates
    widgets = {
        "News": {"id": 22, "type": "news", "data": fetch_news()},
    }

    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

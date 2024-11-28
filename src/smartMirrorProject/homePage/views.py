from django.shortcuts import render
import requests
import json

# Settings for all widgets
API_TIMEOUT = 10

# Weather widget settings
WEATHER_NUMBER_OF_DAYS = 2

# News widget settings
NEWS_NUMBER_OF_ARTICLES = 2

# Time widget settings
TIME_ZONE = "CET"

# Travel widget settings
TRAVEL_BEGIN_STATION = "DID"
TRAVEL_END_STATION = "AH"
TRAVEL_NUMBER_OF_TRIPS = 2

def index(request):
    """
    Renders the homepage with the specified widgets. Each widget needs these keys: 
        id (int): The widget ID.
        type (str): The type of the widget.
        data (dict): The weather data fetched from the API.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage with the widgets context.
    """
    # store the timezone in the session, so it can be accessed by the time widget app
    request.session['timezone'] = TIME_ZONE
    widgets = {
        "weather": {
            "id": 1,
            "type": "weather",
            "data": requests.get(f"http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}", timeout=API_TIMEOUT).json(),
        },
        "news": {
            "id": 2,
            "type": "news",
            "data": requests.get(f"http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}", timeout=API_TIMEOUT).json(),
        },
        "travel": {
            "id": 3,
            "type": "travel",
            "data": requests.get(f"http://localhost:8000/api/travel/fetch/{TRAVEL_BEGIN_STATION}/{TRAVEL_END_STATION}/{TRAVEL_NUMBER_OF_TRIPS}", timeout=API_TIMEOUT).json(),
        },
        "music": {
            "id": 4,
            "type": "music",
            "data": ""
        },
        "time": {
            "id": 5,
            "type": "time",
            "data": requests.get(f"http://localhost:8000/api/time/fetch/{TIME_ZONE}", timeout=API_TIMEOUT).json(),
        },
        "agenda": {
            "id": 6,
            "type": "agenda",
            "data": requests.get("http://localhost:8000/api/agenda/fetch/", timeout=API_TIMEOUT).json()["events"],
        }
    }

    context = {"widgets": widgets}
    return render(request, 'homePage/index.html', context)

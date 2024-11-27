from django.shortcuts import render
import requests

# Settings for all widgets
API_TIMEOUT = 10

# Weather widget settings
WEATHER_NUMBER_OF_DAYS = 2

# News widget settings
NEWS_NUMBER_OF_ARTICLES = 2


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
        }
    }

    context = {"widgets": widgets}
    return render(request, 'homePage/index.html', context)

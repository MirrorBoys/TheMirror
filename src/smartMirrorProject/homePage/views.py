from django.shortcuts import render
import requests

# Settings for all widgets
API_TIMEOUT = 10

# Weather widget settings
WEATHER_NUMBER_OF_DAYS = 2

# News widget settings
NEWS_NUMBER_OF_ARTICLES = 2

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
        "Weather": {
            "id": 1,
            "type": "weather",
            "data": requests.get(f"http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}", timeout=API_TIMEOUT).json(),
        },
        "News": {
            "id": 2,
            "type": "news",
            "data": requests.get(f"http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}", timeout=API_TIMEOUT).json(),
        },	
    }

    context = {"widgets": widgets}
    return render(request, 'homePage/index.html', context)

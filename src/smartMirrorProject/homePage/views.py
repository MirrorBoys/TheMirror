from django.shortcuts import render
import requests

# Settings for all widgets
API_TIMEOUT = 10

# Weather widget settings
WEATHER_NUMBER_OF_DAYS = 2

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
    }

    context = {"widgets": widgets}
    return render(request, 'homePage/index.html', context)

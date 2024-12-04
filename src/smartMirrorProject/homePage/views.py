from django.shortcuts import render
import requests

# Settings for all widgets
API_TIMEOUT = 10

# Weather widget settings
WEATHER_NUMBER_OF_DAYS = 2

# News widget settings
NEWS_NUMBER_OF_ARTICLES = 2


# Travel widget settings
TRAVEL_JOURNEY_BEGIN_STATION = "DID"
TRAVEL_JOURNEY_END_STATION = "AH"
TRAVEL_JOURNEY_NUMBER_OF_TRIPS = 2
TRAVEL_DEPARTURES_STATION = "AH"
# String containing the stations to filter on, separated by a hyphen. If "", no filter is applied.
TRAVEL_DEPARTURES_FILTER = "Nijmegen-Winterswijk-Doetinchem"

# Notes widget settings
NOTE_TITLE = "Sample Note Title"
# html tag (e.g. "ul" or "ol")
NOTE_TYPE = "ul"
# html tag (optional, e.g. "li" which is needed in combination with "ul" or "ol"), leave empty ("") if not needed
NOTE_SUB_TYPE = "li"
# Add your content here. Each line will be rendered as a separate paragraph.
NOTE_CONTENT = [
    "test test test test test test test test test test test test test test test test test test test test test",
    "It can have multiple lines, paragraphs, bulletpoints etc."
]

def index(request):
    """
    Renders the homepage with the specified widgets. Each widget needs these keys: 
        id (int): The widget ID.
        appName (str): The name of the app.
        templateName (str): The name of the used template.
        data (dict): The weather data fetched from the API.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage with the widgets context.
    """
    widgets = {
        "weather": {
            "id": 1,
            "appName": "weatherWidget",
            "templateName": "weather",
            "data": requests.get(f"http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}", timeout=API_TIMEOUT).json(),
        },
        "news": {
            "id": 2,
            "appName": "newsWidget",
            "templateName": "news",
            "data": requests.get(f"http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}", timeout=API_TIMEOUT).json(),
        },
        "travel-journeys": {
            "id": 3,
            "appName": "travelWidget",
            "templateName": "travel-journeys",
            "data": requests.get(f"http://localhost:8000/api/travel/fetch/journeys/{TRAVEL_JOURNEY_BEGIN_STATION}/{TRAVEL_JOURNEY_END_STATION}/{TRAVEL_JOURNEY_NUMBER_OF_TRIPS}", timeout=API_TIMEOUT).json(),
        },
        "travel-departures": {
            "id": 4,
            "appName": "travelWidget",
            "templateName": "travel-departures",
            "data": requests.get(f"http://localhost:8000/api/travel/fetch/departures/{TRAVEL_DEPARTURES_STATION}/{TRAVEL_DEPARTURES_FILTER}", timeout=API_TIMEOUT).json(),
        },
        "music": {
            "id": 5,
            "appName": "musicWidget",
            "templateName": "music",
            "data": ""
        },
        "agenda": {
            "id": 6,
            "appName": "agendaWidget",
            "templateName": "agenda",
            "data": requests.get("http://localhost:8000/api/agenda/fetch/", timeout=API_TIMEOUT).json()["events"],
        },
        "notes": {
            "id": 8,
            "appName": "noteWidget",
            "templateName": "notes",
            "data": {
                "title": NOTE_TITLE,
                "type": NOTE_TYPE,
                "subType": NOTE_SUB_TYPE,
                "content": NOTE_CONTENT
            }
        }
    }

    context = {"widgets": widgets}
    return render(request, 'homePage/index.html', context)

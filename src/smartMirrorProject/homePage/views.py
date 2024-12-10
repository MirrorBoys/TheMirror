from django.shortcuts import render
import requests
import os
import yaml

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yml")
with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG = yaml.safe_load(file)

# Settings for all widgets
API_TIMEOUT = CONFIG["general_settings"]["API_TIMEOUT"]

# Weather widget settings
WEATHER_NUMBER_OF_DAYS = CONFIG["weather"]["WEATHER_NUMBER_OF_DAYS"]

# News widget settings
NEWS_NUMBER_OF_ARTICLES = CONFIG["news"]["NEWS_NUMBER_OF_ARTICLES"]

# Time widget settings
TIME_TIMEZONE = CONFIG["time"]["TIMEZONE"]
TIME_ENCODED_TIMEZONE = TIME_TIMEZONE.replace("/", "-")

# Travel journeys widget settings
TRAVEL_JOURNEY_BEGIN_STATION = CONFIG["travel_journeys"]["TRAVEL_JOURNEY_BEGIN_STATION"]
TRAVEL_JOURNEY_END_STATION = CONFIG["travel_journeys"]["TRAVEL_JOURNEY_END_STATION"]
TRAVEL_JOURNEY_NUMBER_OF_TRIPS = CONFIG["travel_journeys"][
    "TRAVEL_JOURNEY_NUMBER_OF_TRIPS"
]

# Travel departures widget settings
TRAVEL_DEPARTURES_STATION = CONFIG["travel_departures"]["TRAVEL_DEPARTURES_STATION"]
TRAVEL_DEPARTURES_FILTER = CONFIG["travel_departures"]["TRAVEL_DEPARTURES_FILTER"]

# Radar widget settings
RADAR_CITY = CONFIG["radar"]["RADAR_CITY"]

INTERNAL_API_LINKS = {
    "agenda": "http://localhost:8000/api/agenda/fetch/",
    "news": f"http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}",
    "travel_journeys": f"http://localhost:8000/api/travel/fetch/journeys/{TRAVEL_JOURNEY_BEGIN_STATION}/{TRAVEL_JOURNEY_END_STATION}/{TRAVEL_JOURNEY_NUMBER_OF_TRIPS}",
    "travel_departures": f"http://localhost:8000/api/travel/fetch/departures/{TRAVEL_DEPARTURES_STATION}/{TRAVEL_DEPARTURES_FILTER}",
    "weather": f"http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}",
    "radar": f"http://localhost:8000/api/radar/fetch/coordinates/{RADAR_CITY}",
    "time": f"http://localhost:8000/api/time/fetch/{TIME_ENCODED_TIMEZONE}",
}

AVAILABLE_INDEX = [0, 1, 2, 3, 4, 5, 6, 7]


def createWidgetsObject(config, api_links, api_timeout, indexList):
    """
    Creates a dictionary of widget objects based on the provided configuration.

    Args:
        config (dict): A dictionary containing widget configurations.
        api_links (dict): A dictionary containing API links for each widget.
        api_timeout (int): The timeout value (in seconds) for API requests.

    Returns:
        dict: A dictionary where each key is a widget that contains a dictionary with
              widget settings.
    """
    available_widgets = list(config.keys())
    widgetObject = {}

    # Skip first index because this contains the general_settings
    for widget in available_widgets[1:]:
        if not config[widget]["VISIBLE"]:
            continue

        app_name = generate_app_name(widget)

        # Custom approach to music widget is needed because it does not use an internal API
        if widget == "music":
            widgetObject[widget] = {
                "id": index,
                "appName": app_name,
                "templateName": widget,
            }
        else:
            widgetObject[widget] = {
                "id": index,
                "appName": app_name,
                "templateName": widget,
                "data": "",
                "apiCall": lambda link=api_links[widget]: requests.get(
                    link, timeout=api_timeout
                ).json(),
            }

    return widgetObject


def generate_app_name(widget_name: str):
    """
    Generates an application name based on the provided widget name.

    Args:
        widget_name (str): The name of the widget.

    Returns:
        str: The generated application name.
    """
    app_name = widget_name + "Widget"

    if "_" in widget_name:
        app_name = widget_name.split("_")[0] + "Widget"

    return app_name


def generateId(config):

    used_places = set()
    available_widgets = list(config.keys())

    for widget in available_widgets[1:]:
        if "PLACE" in widget and config[widget]["PLACE"] is not None:
            used_places.add(config[widget]["PLACE"])

    current_place = 0
    placesDict = {}

    for widget in available_widgets[1:]:
        if config[widget]["PLACE"] is None:
            while current_place in used_places:
                current_place += 1
            placesDict[widget] = current_place
            used_places.add(current_place)
        else:
            placesDict[widget] = config[widget]["PLACE"]
    return placesDict


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
    generateId(CONFIG)
    widgets = createWidgetsObject(
        CONFIG, INTERNAL_API_LINKS, API_TIMEOUT, AVAILABLE_INDEX
    )

    # Using the internal API's, generate data for each widget.
    # Skip generation of data for music widget since it does not use internal generated data
    for widget in widgets.values():
        if widget["appName"] == "musicWidget":
            continue

        widget["data"] = widget["apiCall"]()

    context = {"widgets": widgets}
    return render(request, "homePage/index.html", context)

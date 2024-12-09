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
TIMEZONE = "Europe/Amsterdam"  # use TZ identifier (e.g. Europe/Amsterdam) or TZ database name (e.g. CET)
ENCODED_TIMEZONE = TIMEZONE.replace("/", "-")

# Travel widget settings

TRAVEL_JOURNEY_BEGIN_STATION = CONFIG["travel_journeys"]["TRAVEL_JOURNEY_BEGIN_STATION"]
TRAVEL_JOURNEY_END_STATION = CONFIG["travel_journeys"]["TRAVEL_JOURNEY_END_STATION"]
TRAVEL_JOURNEY_NUMBER_OF_TRIPS = CONFIG["travel_journeys"][
    "TRAVEL_JOURNEY_NUMBER_OF_TRIPS"
]

TRAVEL_DEPARTURES_STATION = CONFIG["travel_departures"]["TRAVEL_DEPARTURES_STATION"]
# String containing the stations to filter on, separated by a hyphen. If "", no filter is applied.
TRAVEL_DEPARTURES_FILTER = CONFIG["travel_departures"]["TRAVEL_DEPARTURES_FILTER"]

RADAR_CITY = "Arnhem"

INTERNAL_API_LINKS = {
    "agenda": "http://localhost:8000/api/agenda/fetch/",
    "news": f"http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}",
    "travel_journeys": f"http://localhost:8000/api/travel/fetch/journeys/{TRAVEL_JOURNEY_BEGIN_STATION}/{TRAVEL_JOURNEY_END_STATION}/{TRAVEL_JOURNEY_NUMBER_OF_TRIPS}",
    "travel_departures": f"http://localhost:8000/api/travel/fetch/departures/{TRAVEL_DEPARTURES_STATION}/{TRAVEL_DEPARTURES_FILTER}",
    "weather": f"http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}",
}


def createWidget(config, api_links, api_timeout):

    top_level_keys = list(config.keys())
    widget = {}
    currentId = 1

    for key in top_level_keys[1:]:
        if config[key]["VISIBLE"] and key != "music":
            if "_" in key:
                appName = key.split("_")[0] + "Widget"
            else:
                appName = key + "Widget"

            widget[key] = {
                "id": currentId,
                "appName": appName,
                "templateName": key,
                "data": "",
                "apiCall": lambda link=api_links[key]: requests.get(
                    link, timeout=api_timeout
                ).json(),
            }

            currentId += 1

        elif config[key]["VISIBLE"] and key == "music":
            widget[key] = {
                "id": currentId,
                "appName": key + "Widget",
                "templateName": key,
                # "data": "",
                # "apiCall": "",
            }
            currentId += 1

    return widget


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

    widgets = createWidget(CONFIG, INTERNAL_API_LINKS, API_TIMEOUT)

    for widget in widgets.values():
        if widget["templateName"] != "music":
            widget["data"] = widget["apiCall"]()

        "radar": {
            "id": 7,
            "appName": "radarWidget",
            "templateName": "radar",
            "data": requests.get(f"http://localhost:8000/api/radar/fetch/coordinates/{RADAR_CITY}", timeout=API_TIMEOUT).json(),
        }
    }

    context = {"widgets": widgets}
    return render(request, "homePage/index.html", context)

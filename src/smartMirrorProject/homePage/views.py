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


# Travel widget settings
TRAVEL_JOURNEY_BEGIN_STATION = CONFIG["travel_journeys"]["TRAVEL_JOURNEY_BEGIN_STATION"]
TRAVEL_JOURNEY_END_STATION = CONFIG["travel_journeys"]["TRAVEL_JOURNEY_END_STATION"]
TRAVEL_JOURNEY_NUMBER_OF_TRIPS = CONFIG["travel_journeys"][
    "TRAVEL_JOURNEY_NUMBER_OF_TRIPS"
]

TRAVEL_DEPARTURES_STATION = CONFIG["travel_departures"]["TRAVEL_DEPARTURES_STATION"]
# String containing the stations to filter on, separated by a hyphen. If "", no filter is applied.
TRAVEL_DEPARTURES_FILTER = CONFIG["travel_departures"]["TRAVEL_DEPARTURES_FILTER"]


INTERNAL_API_LINKS = {
    "agenda": "http://localhost:8000/api/agenda/fetch/",
    "news": "http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}",
    "travel_journeys": "http://localhost:8000/api/travel/fetch/journeys/{TRAVEL_JOURNEY_BEGIN_STATION}/{TRAVEL_JOURNEY_END_STATION}/{TRAVEL_JOURNEY_NUMBER_OF_TRIPS}",
    "travel_departures": "http://localhost:8000/api/travel/fetch/departures/{TRAVEL_DEPARTURES_STATION}/{TRAVEL_DEPARTURES_FILTER}",
    "weather": "http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}",
}


def createWidget(config, api_links, api_timeout):

    top_level_keys = list(config.keys())
    widget = {}
    currentId = 1

    for key in top_level_keys[1:]:
        if config[key]["VISIBLE"] and key != "spotify":

            api_string = (
                f"requests.get("
                f"'{api_links[key]}', "
                f"timeout={api_timeout}"
                f").json()"
            )

            widget[key] = {
                "id": currentId,
                "appName": key + "Widget",
                "templateName": key,
                "data": api_string,
            }

            currentId += 1
        elif config[key]["VISIBLE"] and key == "spotify":
            widget[key] = {
                "id": currentId,
                "appName": key + "Widget",
                "templateName": key,
                "data": "",
            }
            currentId += 1

    print(widget)
    return widget


widgets = createWidget(CONFIG, INTERNAL_API_LINKS, API_TIMEOUT)


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
    # widgets = {
    #     "weather": {
    #         "id": 1,
    #         "appName": "weatherWidget",
    #         "templateName": "weather",
    #         "data": requests.get(
    #             f"http://localhost:8000/api/weather/fetch/{WEATHER_NUMBER_OF_DAYS}",
    #             timeout=API_TIMEOUT,
    #         ).json(),
    #     },
    #     "news": {
    #         "id": 2,
    #         "appName": "newsWidget",
    #         "templateName": "news",
    #         "data": requests.get(
    #             f"http://localhost:8000/api/news/fetch/{NEWS_NUMBER_OF_ARTICLES}",
    #             timeout=API_TIMEOUT,
    #         ).json(),
    #     },
    #     "travel_journeys": {
    #         "id": 3,
    #         "appName": "travelWidget",
    #         "templateName": "travel_journeys",
    #         "data": requests.get(
    #             f"http://localhost:8000/api/travel/fetch/journeys/{TRAVEL_JOURNEY_BEGIN_STATION}/{TRAVEL_JOURNEY_END_STATION}/{TRAVEL_JOURNEY_NUMBER_OF_TRIPS}",
    #             timeout=API_TIMEOUT,
    #         ).json(),
    #     },
    #     "travel_departures": {
    #         "id": 4,
    #         "appName": "travelWidget",
    #         "templateName": "travel_departures",
    #         "data": requests.get(
    #             f"http://localhost:8000/api/travel/fetch/departures/{TRAVEL_DEPARTURES_STATION}/{TRAVEL_DEPARTURES_FILTER}",
    #             timeout=API_TIMEOUT,
    #         ).json(),
    #     },
    #     "music": {
    #         "id": 5,
    #         "appName": "musicWidget",
    #         "templateName": "music",
    #         "data": "",
    #     },
    #     "agenda": {
    #         "id": 6,
    #         "appName": "agendaWidget",
    #         "templateName": "agenda",
    #         "data": requests.get(
    #             "http://localhost:8000/api/agenda/fetch/", timeout=API_TIMEOUT
    #         ).json()["events"],
    #     },
    # }

    context = {"widgets": widgets}
    return render(request, "homePage/index.html", context)

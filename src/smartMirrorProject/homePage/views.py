import requests
import os
import yaml
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def getUserName(request):
    """
    Retrieves the username of the currently logged in user.
    """
    if request and request.user.is_authenticated:
        return request.user.username
    return ""


def getConfigFile(username):
    """
    Retrieves the config file based on the username

    Args:
        Username (str)

    Returns:
        (dict): A dictionary containing widget configurations.
    """
    configFileName = username + "_config.yml"
    filePath = os.path.join(os.path.dirname(__file__), "..", configFileName)
    with open(filePath, "r") as file:
        config = yaml.safe_load(file)
        print(config)
    return config


def getGeneralSettings(config):
    """
    Gets the Api timeout from the config file.

    Args:
        config (dict): A dictionary containing widget configurations.

    """
    # Settings for all widgets
    API_TIMEOUT = config["general_settings"]["API_TIMEOUT"]
    return API_TIMEOUT


def createApiLinks(config):
    """
    Creates a dictionary of the different internal api links with the provided configuration.

    Args:
        config (dict): A dictionary containing widget configurations.

    Returns:
        dict: A dictionary where each key is a widget and contains the internal api link.
    """

    TIME_TIMEZONE = config["time"]["TIMEZONE"]
    TIME_ENCODED_TIMEZONE = TIME_TIMEZONE.replace("/", "-")

    API_LINKS = {
        "agenda": "http://localhost:8000/api/agenda/fetch/",
        "news": f"http://localhost:8000/api/news/fetch/{config["news"]["NEWS_NUMBER_OF_ARTICLES"]}",
        "note": "http://localhost:8000/api/note/fetch/",
        "travel_journeys": f"http://localhost:8000/api/travel/fetch/journeys/{config["travel_journeys"]["TRAVEL_JOURNEY_BEGIN_STATION"]}/{config["travel_journeys"]["TRAVEL_JOURNEY_END_STATION"]}/{config["travel_journeys"]["TRAVEL_JOURNEY_NUMBER_OF_TRIPS"]}",
        "travel_departures": f"http://localhost:8000/api/travel/fetch/departures/{config["travel_departures"]["TRAVEL_DEPARTURES_STATION"]}/{config["travel_departures"]["TRAVEL_DEPARTURES_FILTER"]}",
        "weather": f"http://localhost:8000/api/weather/fetch/{config["weather"]["WEATHER_NUMBER_OF_DAYS"]}",
        "radar": f"http://localhost:8000/api/radar/fetch/coordinates/{config["radar"]["RADAR_CITY"]}",
        "time": f"http://localhost:8000/api/time/fetch/{TIME_ENCODED_TIMEZONE}",
    }
    return API_LINKS


def createWidgetsObject(config, api_links, api_timeout):
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
    for index, widget in enumerate(available_widgets[1:]):
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


@login_required
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
    username = getUserName(request)

    config = getConfigFile(username)

    internalApiLinks = createApiLinks(config)

    apiTimeout = getGeneralSettings(config)

    widgets = createWidgetsObject(config, internalApiLinks, apiTimeout)

    # Using the internal API's, generate data for each widget.
    # Skip generation of data for music widget since it does not use internal generated data
    for widget in widgets.values():
        if widget["appName"] == "musicWidget":
            continue

        widget["data"] = widget["apiCall"]()

    context = {"widgets": widgets}
    return render(request, "homePage/index.html", context)

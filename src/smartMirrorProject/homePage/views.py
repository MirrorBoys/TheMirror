import requests
import os
import yaml
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def get_username(request):
    """
    Retrieves the username of the currently logged in user.
    """
    if request and request.user.is_authenticated:
        return request.user.username
    return ""


def get_config_file(username):
    """
    Retrieves the config file based on the username

    Args:
        Username (str)

    Returns:
        (dict): A dictionary containing widget configurations.
    """
    config_file_name = username + "_config.yml"
    file_path = os.path.join(
        os.path.dirname(__file__), "..", "config", config_file_name
    )
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def get_general_settings(config):
    """
    Gets the Api timeout from the config file.

    Args:
        config (dict): A dictionary containing widget configurations.

    """
    # Settings for all widgets
    general_settings = config["general_settings"]
    return general_settings


def create_api_links(config):
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
        "agenda": "http://localhost:8000/api/agenda/fetch",
        "news": f"http://localhost:8000/api/news/fetch/{config['news']['NEWS_NUMBER_OF_ARTICLES']}",
        "note": "http://localhost:8000/api/note/fetch/",
        "travel_journeys": f"http://localhost:8000/api/travel/fetch/journeys/{config['travel_journeys']['TRAVEL_JOURNEY_BEGIN_STATION']}/{config['travel_journeys']['TRAVEL_JOURNEY_END_STATION']}/{config['travel_journeys']['TRAVEL_JOURNEY_NUMBER_OF_TRIPS']}",
        "travel_departures": f"http://localhost:8000/api/travel/fetch/departures/{config['travel_departures']['TRAVEL_DEPARTURES_STATION']}/{config['travel_departures']['TRAVEL_DEPARTURES_FILTER']}",
        "weather": f"http://localhost:8000/api/weather/fetch/{config['weather']['WEATHER_NUMBER_OF_DAYS']}",
        "radar": f"http://localhost:8000/api/radar/fetch/coordinates/{config['radar']['RADAR_CITY']}",
        "time": f"http://localhost:8000/api/time/fetch/{TIME_ENCODED_TIMEZONE}",
    }
    return API_LINKS


def create_widgets_object(config, api_links, api_timeout):
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
    widget_object = {}

    # Skip first index because this contains the general_settings
    for widget in available_widgets[1:]:
        if not config[widget]["VISIBLE"]:
            continue

        app_name = generate_app_name(widget)

        # Only add apiCall to widgets that need aditional data and thus use an internal API key.
        if widget in api_links:
            widget_object[widget] = {
                "id": index,
                "appName": app_name,
                "templateName": widget,
                "data": "",
                "apiCall": lambda link=api_links[widget]: requests.get(
                    link, timeout=api_timeout
                ).json(),
            }
        else:
            widget_object[widget] = {
                "id": index,
                "appName": app_name,
                "templateName": widget,
            }

    return widget_object


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
    username = get_username(request)

    config = get_config_file(username)

    internal_api_links = create_api_links(config)

    general_settings = get_general_settings(config)

    api_timeout = general_settings["API_TIMEOUT"]

    widgets = create_widgets_object(config, internal_api_links, api_timeout)

    # Using the internal API's, generate data for each widget.
    # Skip generation of data for music widget since it does not use internal generated data
    widgets_to_delete = []
    for widget in widgets.values():
        if "apiCall" not in widget:
            continue

        try:
            widget["data"] = widget["apiCall"]()
        except Exception as e:
            widgets_to_delete.append(widget["templateName"])

    for widget_name in widgets_to_delete:
        del widgets[widget_name]

    context = {"widgets": widgets}
    return render(request, "homePage/index.html", context)

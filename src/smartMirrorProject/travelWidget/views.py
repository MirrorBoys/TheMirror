from datetime import datetime
import os
import requests
from django.http import JsonResponse

NS_KEY = os.getenv("NS_KEY")


def calculate_delay(planned, actual):
    """
    Helper function to calculate delay

    Args:
        planned (str): The planned time in ISO format (YYYY-MM-DDTHH:MM:SS).
        actual (str): The actual time in ISO format (YYYY-MM-DDTHH:MM:SS).

    Returns:
        str: The delay in minutes as a string with a "+" prefix if there is a delay,
             "On time" if there is no delay, or "N/A" if either planned or actual time is not provided.
    """
    if not planned or not actual:
        return "N/A"
    planned_time = datetime.fromisoformat(planned)
    actual_time = datetime.fromisoformat(actual)
    delay_minutes = (actual_time - planned_time).total_seconds() / 60
    return f"+{int(delay_minutes)} min" if delay_minutes > 0 else "On time"


def format_time(time_str):
    """
    Converts an ISO format time string to a formatted time string.

    Args:
        time_str (str): The time string in ISO format.

    Returns:
        str: The formatted time string in "HH:MM:SS" format. If the input is None or invalid, returns "N/A".
    """
    if not time_str:
        return "N/A"
    try:
        # Convert from ISO format string to time
        time = datetime.fromisoformat(time_str)
        return time.strftime("%H:%M:%S")  # Format as HH:mm:ss
    except Exception:
        return "N/A"


def fetch_trip(request, start_station, end_station, amount_trips):
    """
    Fetches trip information from the NS API and returns it as a JSON response. The codes for the stations can be retrieved with the NS API (https://apiportal.ns.nl/api-details#api=reisinformatie-api&operation=getStations).
    We've saved a csv file with the station codes in Teams (Algemeen/NS_API).

    Args:
        request: The HTTP request object.
        start_station (str): The starting station code.
        end_station (str): The ending station code.
        amount_trips (int): The number of trips to fetch.

    Returns:
        JsonResponse: A JSON response containing trip information, including station names,
                      planned and actual departure/arrival times, delays, and whether the station
                      is the final station of the trip.
    """
    # Build the URL dynamically using f-string (no parentheses)
    url = (
        f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips?"
        f"fromStation={start_station}&toStation={end_station}&originWalk=false&originBike=false&originCar=false&"
        f"destinationWalk=false&destinationBike=false&destinationCar=false&shorterChange=false&"
        f"travelAssistance=false&searchForAccessibleTrip=false&localTrainsOnly=false&"
        f"excludeHighSpeedTrains=false&excludeTrainsWithReservationRequired=false&discount=NO_DISCOUNT&"
        f"travelClass=2&passing=false&travelRequestType=DEFAULT"
    )

    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": NS_KEY,
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Extract relevant data from the response
        travelData = {
            "first_station": start_station,
            "last_station": end_station,
            "trips": [],
        }

        for trip in data.get("trips", [])[:amount_trips]:
            trip_data = {"stations": []}

            for leg in trip.get("legs", []):
                stops = leg.get("stops", [])
                for idx, stop in enumerate(stops):
                    station_name = stop.get("name")
                    planned_departure = stop.get("plannedDepartureDateTime")
                    actual_departure = stop.get("actualDepartureDateTime")
                    planned_arrival = stop.get("plannedArrivalDateTime")
                    actual_arrival = stop.get("actualArrivalDateTime")

                    # Calculate delay before formatting the times
                    delay = calculate_delay(
                        planned_arrival if idx == len(stops) - 1 else planned_departure,
                        actual_arrival if idx == len(stops) - 1 else actual_departure,
                    )

                    # Format times after delay calculation
                    formatted_planned_departure = format_time(planned_departure)
                    formatted_actual_departure = format_time(actual_departure)
                    formatted_planned_arrival = format_time(planned_arrival)
                    formatted_actual_arrival = format_time(actual_arrival)

                    # Determine if this is the final station of the trip
                    is_final_station = idx == len(stops) - 1

                    # Add the formatted times and other data to the stations list
                    trip_data["stations"].append(
                        {
                            "station": station_name,
                            "planned_departure": formatted_planned_departure,
                            "actual_departure": formatted_actual_departure,
                            "planned_arrival": formatted_planned_arrival,
                            "actual_arrival": formatted_actual_arrival,
                            "is_final_station": is_final_station,
                            "delay": delay,
                        }
                    )

            travelData["trips"].append(trip_data)

        return JsonResponse(travelData)

    except Exception as e:
        print(f"Error fetching NS API: {e}")
        return JsonResponse({"error": "Unable to fetch travel information."})


def fetch_ns_stations(api_key):
    """
    Get the station information from the NS API.

    :param api_key: The NS API-key for authentication.
    :return: JSON-object with station information.
    """
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations"
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["payload"]


def extract_nl_station_names_and_codes(payload):
    """
    get only the dutch station names and codes from the NS API.

    :param payload: the json with the response from
    :return: A list of tuples with station names and their code.
    """
    nl_stations = []
    for station in payload:
        if station.get("land") == "NL":  # Controleer op landcode NL
            full_name = station.get("namen", {}).get("lang", "Onbekende naam")
            code = station.get("code", "Geen code")
            nl_stations.append((full_name, code))
    return nl_stations


def get_station_name_by_code(station_code, stations):
    """
    Gets the name of a station from the given station code.

    :param station_code: The station code.
    :param stations: A list with tuples with station names and codes
    :return: The name of a station as string, of None is the code is not found
    """
    for name, code in stations:
        if code == station_code:
            return name
    return None


def fetch_departures(request, station, destination_filter=None):
    """
    Fetches train departure information from the NS API for a given station and optionally filters by destination.
    Args:
        request: The HTTP request object.
        station (str): The station code for which to fetch departure information.
        destination_filter (str, optional): A string of destination names to filter the departures. Defaults to None.
    Returns:
        JsonResponse: A JSON response containing a list of departures with the following fields:
            - destination (str): The destination of the train.
            - trainCategory (str): The category of the train.
            - plannedDateTime (str): The planned departure time, formatted.
            - actualDateTime (str): The actual departure time, formatted.
            - delay (str): The delay in departure time.
            - plannedTrack (str): The planned track for the departure.
    """
    # The destination_filter is converted from a string to a list
    if destination_filter is not None:
        destination_filter = destination_filter.split("-")

    url = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/departures?station={station}"

    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": NS_KEY,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 401)

        data = response.json()  # Parse the JSON response
        # print(data) # debug

        departures = []

        for departure in data.get("payload", {}).get("departures", []):
            destination = departure.get("direction")
            # If destination_filter is provided and is not a list, convert it to a list
            if destination_filter:
                if isinstance(destination_filter, str):
                    destination_filter = [
                        destination_filter
                    ]  # Convert to list if it's a single string

                if destination not in destination_filter:
                    continue  # Skip this departure if it doesn't match any destination in the filter

            trainCategory = departure.get("trainCategory")
            planned_departure = departure.get("plannedDateTime")
            actual_departure = departure.get("actualDateTime")
            planned_track = departure.get("plannedTrack")

            delay = calculate_delay(planned_departure, actual_departure)

            formatted_planned_departure = format_time(planned_departure)
            formatted_actual_departure = format_time(actual_departure)

            # Extract the desired fields for each departure
            departures.append(
                {
                    "destination": destination,
                    "trainCategory": trainCategory,
                    "plannedDateTime": formatted_planned_departure,
                    "actualDateTime": formatted_actual_departure,
                    "delay": delay,
                    "plannedTrack": planned_track,
                }
            )

            list_of_stations = fetch_ns_stations(NS_KEY)
            list_of_nl_stations = extract_nl_station_names_and_codes(list_of_stations)
            station_name = get_station_name_by_code(station, list_of_nl_stations)

        return JsonResponse(
            {"station": station, "station_name": station_name, "departures": departures}
        )  # Include station at the top level

    except requests.exceptions.RequestException as e:
        print(f"Error fetching departures: {e}")
        return JsonResponse({"station": station, "departures": []})

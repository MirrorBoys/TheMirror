from datetime import datetime
import requests
from django.http import JsonResponse

# NS_KEY = os.getenv("NS_KEY")
NS_KEY = "1ccd5d99ee5d47668909933a5c848db4"

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
            "trips": []
        }

        for trip in data.get("trips", [])[:amount_trips]:
            trip_data = {
                "stations": []
            }

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

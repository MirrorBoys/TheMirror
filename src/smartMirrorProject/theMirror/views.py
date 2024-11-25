import feedparser
from django.http import HttpResponse
from django.shortcuts import render
import requests
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()

NS_KEY = os.getenv('NS_KEY')

# Helper function to calculate delay
def calculate_delay(planned, actual):
    if not planned or not actual:
        return "N/A"
    planned_time = datetime.fromisoformat(planned)
    actual_time = datetime.fromisoformat(actual)
    delay_minutes = (actual_time - planned_time).total_seconds() / 60
    return f"+{int(delay_minutes)} min" if delay_minutes > 0 else "On time"

# Helper function to format the time
def format_time(time_str):
    if not time_str:
        return "N/A"
    try:
        # Convert from ISO format string to time
        time = datetime.fromisoformat(time_str)
        return time.strftime("%H:%M:%S")  # Format as HH:mm:ss
    except Exception:
        return "N/A"

def fetch_reisplanner(start_station, end_station, amount_trips):
    # Build the URL dynamically using f-string (no parentheses)
    url = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips?" \
          f"fromStation={start_station}&toStation={end_station}&originWalk=false&originBike=false&originCar=false&" \
          f"destinationWalk=false&destinationBike=false&destinationCar=false&shorterChange=false&" \
          f"travelAssistance=false&searchForAccessibleTrip=false&localTrainsOnly=false&" \
          f"excludeHighSpeedTrains=false&excludeTrainsWithReservationRequired=false&discount=NO_DISCOUNT&" \
          f"travelClass=2&passing=false&travelRequestType=DEFAULT"

    headers = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': NS_KEY,
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Extract relevant data from the response
        trips = []
        for trip in data.get("trips", [])[:amount_trips]:
            first_station = trip["legs"][0]["stops"][0]["name"]  # First station
            last_station = trip["legs"][-1]["stops"][-1]["name"]  # Last station

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
                        actual_arrival if idx == len(stops) - 1 else actual_departure
                    )

                    # Format times after delay calculation
                    formatted_planned_departure = format_time(planned_departure)
                    formatted_actual_departure = format_time(actual_departure)
                    formatted_planned_arrival = format_time(planned_arrival)
                    formatted_actual_arrival = format_time(actual_arrival)

                    # Determine if this is the final station of the trip
                    is_final_station = idx == len(stops) - 1
                    
                    # Add the formatted times and other data to the trips list
                    trips.append({
                        "station": station_name,
                        "planned_departure": formatted_planned_departure,
                        "actual_departure": formatted_actual_departure,
                        "planned_arrival": formatted_planned_arrival,
                        "actual_arrival": formatted_actual_arrival,
                        "is_final_station": is_final_station,
                        "delay": delay,
                        "first_station": first_station,
                        "last_station": last_station,
                    })

        return trips

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NS API: {e}")
        return [{"error": "Unable to fetch travel information."}]



def fetch_news():
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    news_data = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:2]]
    return news_data

def time_api(request):
    response = requests.get(
        "https://www.timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam",
        timeout=10,
    )
    data = response.json()
    time_data = {
        "time": data["time"],
        "seconds": data["seconds"],
        "date": data["date"],
        "dayOfWeek": data["dayOfWeek"],
    }
    return time_data

def index(request):
    # Example data with widget types or specific templates
    widgets = {
        "Weather_1": {
            "id": 1,
            "type": "weather",
            "data": {"temperature": 22, "condition": "Sunny"},
        },
        "Weather_2": {
            "id": 2,
            "type": "weather",
            "data": {"temperature": 18, "condition": "Cloudy"},
        },
        "Weather_3": {
            "id": 3,
            "type": "weather",
            "data": {"temperature": 25, "condition": "Rainy"},
        },
        "Weather_4": {
            "id": 4,
            "type": "weather",
            "data": {"temperature": 30, "condition": "Sunny"},
        },
        "Weather_5": {
            "id": 5,
            "type": "weather",
            "data": {"temperature": 20, "condition": "Windy"},
        },
        "Weather_6": {
            "id": 6,
            "type": "weather",
            "data": {"temperature": 17, "condition": "Snowy"},
        },
        "Weather_7": {
            "id": 7,
            "type": "weather",
            "data": {"temperature": 24, "condition": "Cloudy"},
        },
        "Weather_8": {
            "id": 8,
            "type": "weather",
            "data": {"temperature": 27, "condition": "Sunny"},
        },
        "Weather_9": {
            "id": 9,
            "type": "weather",
            "data": {"temperature": 19, "condition": "Rainy"},
        },
        "Weather_10": {
            "id": 10,
            "type": "weather",
            "data": {"temperature": 21, "condition": "Windy"},
        },
        "Weather_11": {
            "id": 11,
            "type": "weather",
            "data": {"temperature": 23, "condition": "Sunny"},
        },
        "Weather_12": {
            "id": 12,
            "type": "weather",
            "data": {"temperature": 26, "condition": "Cloudy"},
        },
        "Weather_13": {
            "id": 13,
            "type": "weather",
            "data": {"temperature": 22, "condition": "Rainy"},
        },
        "Weather_14": {
            "id": 14,
            "type": "weather",
            "data": {"temperature": 29, "condition": "Sunny"},
        },
        "Weather_15": {
            "id": 15,
            "type": "weather",
            "data": {"temperature": 28, "condition": "Windy"},
        },
        "Weather_16": {
            "id": 16,
            "type": "weather",
            "data": {"temperature": 20, "condition": "Snowy"},
        },
        "Weather_17": {
            "id": 17,
            "type": "weather",
            "data": {"temperature": 18, "condition": "Cloudy"},
        },
        "Weather_18": {
            "id": 18,
            "type": "weather",
            "data": {"temperature": 25, "condition": "Rainy"},
        },
        "Weather_19": {
            "id": 19,
            "type": "weather",
            "data": {"temperature": 24, "condition": "Sunny"},
        },
        "Travel": {
            "id": 20,
            "type": "travel",
            "data": fetch_reisplanner("DID","AH",1), # vanaf station, naar station, aantal journeys die hij laat zien
        },
        "News": {
            "id": 22,
            "type": "news",
            "data": fetch_news()
        },
        "Time": {
            "type": "time",
            "data": time_api(request)
        },
    }
    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

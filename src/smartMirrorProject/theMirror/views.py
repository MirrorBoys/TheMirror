from django.http import HttpResponse
from django.shortcuts import render

# Multiple widgets
import requests
from datetime import datetime
from . import spotify
import os
from dotenv import load_dotenv

# News widget
import feedparser

# Weather widget
import sys
import locale
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

load_dotenv()


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


NS_KEY = os.getenv("NS_KEY")

def fetch_departures(station, destination_filter=None):
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
                    destination_filter = [destination_filter]  # Convert to list if it's a single string

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
                "plannedDateTime":  formatted_planned_departure,
                "actualDateTime": formatted_actual_departure,
                "delay" : delay,
                "plannedTrack": planned_track,
            })

        return departures  # Return a list of dictionaries with the relevant data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching departures: {e}")
        return []



def fetch_reisplanner(start_station, end_station, amount_trips):
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
                        actual_arrival if idx == len(stops) - 1 else actual_departure,
                    )

                    # Format times after delay calculation
                    formatted_planned_departure = format_time(planned_departure)
                    formatted_actual_departure = format_time(actual_departure)
                    formatted_planned_arrival = format_time(planned_arrival)
                    formatted_actual_arrival = format_time(actual_arrival)

                    # Determine if this is the final station of the trip
                    is_final_station = idx == len(stops) - 1

                    # Add the formatted times and other data to the trips list
                    trips.append(
                        {
                            "station": station_name,
                            "planned_departure": formatted_planned_departure,
                            "actual_departure": formatted_actual_departure,
                            "planned_arrival": formatted_planned_arrival,
                            "actual_arrival": formatted_actual_arrival,
                            "is_final_station": is_final_station,
                            "delay": delay,
                            "first_station": first_station,
                            "last_station": last_station,
                        }
                    )

        return trips

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NS API: {e}")
        return [{"error": "Unable to fetch travel information."}]


def fetch_news():
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    news_data = [
        {"title": entry.title, "link": entry.link} for entry in feed.entries[:2]
    ]
    return news_data


# Weather widget variables. See Teams for API key.
weatherApiKey = None
weatherDatasetName = "outlook_weather_forecast"
weatherDatasetVersion = "1.0"
weatherNumberOfDays = 2


# Code is based on KNMI's example code (https://developer.dataplatform.knmi.nl/open-data-api#example-last)
# Used dataset: https://dataplatform.knmi.nl/dataset/short-term-weather-forecast-1-0
def fetchWeather(apiKey, datasetName, datasetVersion, numberOfDays):
    api = OpenDataAPI(api_token=apiKey)

    # Sort files in descending order and only retrieve the first file
    params = {"maxKeys": 1, "orderBy": "created", "sorting": "desc"}
    response = api.listFiles(datasetName, datasetVersion, params)
    if "error" in response:
        print(f"Unable to retrieve list of files: {response['error']}.")
        sys.exit(1)

    # Download latest available file from the dataset
    latestFile = response["files"][0].get("filename")

    # Get download url and download the file
    response = api.getFileUrl(datasetName, datasetVersion, latestFile)
    downloadFileFromUrl(response["temporaryDownloadUrl"], latestFile)

    # Process file
    weatherData = generateWeatherObject(latestFile, "KNMI", numberOfDays)

    # Delete the file after downloading
    os.remove(latestFile)

    return weatherData


class OpenDataAPI:
    def __init__(self, api_token: str):
        self.baseUrl = "https://api.dataplatform.knmi.nl/open-data/v1"
        self.headers = {"Authorization": api_token}

    def __getData(self, url, params=None):
        return requests.get(url, headers=self.headers, params=params).json()

    def listFiles(self, datasetName: str, datasetVersion: str, params: dict):
        return self.__getData(
            f"{self.baseUrl}/datasets/{datasetName}/versions/{datasetVersion}/files",
            params=params,
        )

    def getFileUrl(self, datasetName: str, datasetVersion: str, fileName: str):
        return self.__getData(
            f"{self.baseUrl}/datasets/{datasetName}/versions/{datasetVersion}/files/{fileName}/url"
        )


def downloadFileFromUrl(downloadUrl, filename):
    try:
        with requests.get(downloadUrl, stream=True) as response:
            # Raise an exception for error status codes
            response.raise_for_status()
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except Exception:
        print(f"An error occurred while downloading the file: {Exception}.")
        sys.exit(1)


def generateWeatherObject(weatherFile, source, numberOfDays):
    # Load XML file and select main element that contains the forecast data
    tree = ET.parse(weatherFile)
    root = tree.getroot()
    forecast = root.find("*")

    # Populate array with data from XML file
    weatherData = {
        "source": source,
        "lastUpdate": forecast.find("tijd_aanmaak").text,
        "expectation": forecast.find("verwachting_meerdaagse").text,
        "dailyForecast": [],
    }

    # Loop through 7 days to populate array with precipitation and temperature for each day
    for index in range(1, numberOfDays + 1):
        dayData = {
            "day": convertDateToRelative(
                forecast.find(f"dag{index}_dddd_dd_mmmm_yyyy").text
            ),
            # "day": forecast.find(f"dag{index}_ddd").text,
            # "day": forecast.find(f"dag{index}_dddd_dd_mmmm_yyyy").text,
            "precipitation": {
                "min": forecast.find(f"neerslaghoeveelheid_min_dag{index}").text,
                "max": forecast.find(f"neerslaghoeveelheid_max_dag{index}").text,
                "chance": forecast.find(f"neerslagkans_dag{index}").text,
            },
            "temperature": {
                "min": forecast.find(f"minimumtemperatuur_min_dag{index}").text,
                "max": forecast.find(f"maximumtemperatuur_max_dag{index}").text,
            },
        }
        weatherData["dailyForecast"].append(dayData)

    return weatherData


def convertDateToRelative(date: str):
    returnValue = ""

    # Change locale to Dutch for correct date formatting
    locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")
    dateFormat = "%A %d %B %Y"
    inputDate = datetime.strptime(date, dateFormat).date()
    today = datetime.today().date()

    if inputDate == today:
        returnValue = "Vandaag"
    elif inputDate == today + timedelta(days=1):
        returnValue = "Morgen"
    elif inputDate == today - timedelta(days=1):
        returnValue = "Gisteren"
    elif inputDate < today:
        daysDifference = today - inputDate
        returnValue = f"{daysDifference.days} dagen geleden"
    else:
        daysDifference = inputDate - today
        returnValue = f"Over {daysDifference.days} dagen"

    return returnValue


def index(request):
    # Example data with widget types or specific templates
    widgets = {
        "Weather": {
            "id": 1,
            "type": "weather",
            "data": fetchWeather(
                weatherApiKey,
                weatherDatasetName,
                weatherDatasetVersion,
                weatherNumberOfDays,
            ),
        },
        "Travel": {
            "id": 2,
            "type": "travel",
            # The codes for the stations can be retrieved with the NS API (https://apiportal.ns.nl/api-details#api=reisinformatie-api&operation=getStations). We've saved
            # an csv file with the station codes in Teams (Algemeen\NS_API)
            "data": fetch_reisplanner(
                "AH", "DID", 1
            ),  # vanaf station, naar station, aantal journeys die hij laat zien
        },
        "Travel2": {
            "id": 3,
            "type": "travel2",
            "data": fetch_departures("AH", destination_filter=["Nijmegen", "Winterswijk", "Doetinchem"]),  # Filter for multiple destinations
            "station": "Arnhem Centraal", # API boodt geen mogelijkheid aan om deze ook aan te roepen helaas
        },
        "News": {"id": 4, "type": "news", "data": fetch_news()},
        "Music": {
            "id": 5,
            "type": "music",
            "data": "",
        },
    }

    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

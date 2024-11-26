from django.http import HttpResponse
from django.shortcuts import render

# Multiple widgets
import requests

# News widget
import feedparser

# Weather widget
import sys
import os
import locale
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET


def fetch_news():
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    news_data = [
        {"title": entry.title, "link": entry.link} for entry in feed.entries[:2]
    ]
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
        "Weather_1": {
            "id": 1,
            "type": "weather",
            "data": fetchWeather(
                weatherApiKey,
                weatherDatasetName,
                weatherDatasetVersion,
                weatherNumberOfDays,
            ),
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
        "Weather_20": {
            "id": 20,
            "type": "weather",
            "data": {"temperature": 21, "condition": "Windy"},
        },
        "News": {"id": 22, "type": "news", "data": fetch_news()},
        "Time": {"type": "time", "data": time_api(request)},
    }
    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

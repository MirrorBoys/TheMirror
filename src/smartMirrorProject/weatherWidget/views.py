from datetime import datetime, timedelta
from django.http import JsonResponse

import sys
import os
import xml.etree.ElementTree as ET
import locale
import requests

KNMI_API_KEY = os.getenv("KNMI_API_KEY")
KNMI_API_DATASET_NAME = "outlook_weather_forecast"
KNMI_API_DATASETVERSION = "1.0"
KNMI_API_TIMEOUT = 10


def fetchWeather(request, numberOfDays):
    """
    Fetches weather data for a specified number of days.

    Code based on KNMI example (https://developer.dataplatform.knmi.nl/open-data-api#example-last)
    Used dataset: https://dataplatform.knmi.nl/dataset/short-term-weather-forecast-1-0

    Args:
        request: The HTTP request object.
        numberOfDays (int): The number of days for which to fetch weather data.

    Returns:
        dict: A dictionary in JSON format containing the processed weather data.
    """
    api = OpenDataAPI(KNMI_API_KEY)

    # Sort files in descending order and only retrieve the first file
    params = {"maxKeys": 1, "orderBy": "created", "sorting": "desc"}
    response = api.listFiles(KNMI_API_DATASET_NAME, KNMI_API_DATASETVERSION, params)
    if "error" in response:
        print(f"Unable to retrieve list of files: {response['error']}.")
        sys.exit(1)

    # Get filename of latest available file from the dataset
    latestFile = response["files"][0].get("filename")

    # Get download url and download the file
    response = api.getFileUrl(
        KNMI_API_DATASET_NAME, KNMI_API_DATASETVERSION, latestFile
    )
    downloadFileFromUrl(response["temporaryDownloadUrl"], latestFile)

    # Process file
    weatherData = generateWeatherJson(latestFile, "KNMI", numberOfDays)

    # Delete file after downloading
    os.remove(latestFile)

    return weatherData


class OpenDataAPI:
    """
    A class to interact with the KNMI Open Data API.

    Attributes:
        api_token (str): The API token for authorization.

    Methods:
        listFiles(datasetName: str, datasetVersion: str, params: dict):
            Lists files available in a specific dataset version.

        getFileUrl(datasetName: str, datasetVersion: str, fileName: str):
            Retrieves the URL for a specific file in a dataset version.
    """

    def __init__(self, api_token: str):
        self.baseUrl = "https://api.dataplatform.knmi.nl/open-data/v1"
        self.headers = {"Authorization": api_token}

    def __getData(self, url, params=None):
        return requests.get(
            url, headers=self.headers, params=params, timeout=KNMI_API_TIMEOUT
        ).json()

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
    """
    Downloads a file from the specified URL and saves it to the given filename.

    Args:
        downloadUrl (str): The URL from which to download the file.
        filename (str): The path where the downloaded file will be saved.
    """
    try:
        with requests.get(downloadUrl, stream=True, timeout=KNMI_API_TIMEOUT) as response:
            # Raise an exception for error status codes
            response.raise_for_status()
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the file: {e}.")
        sys.exit(1)


def generateWeatherJson(weatherFileName, source, numberOfDays):
    """
    Generates a JSON file containing weather forecast data extracted from XML file.

    Args:
        weatherFileName (str): The path to the XML file containing the weather forecast data.
        source (str): The source of the weather data.
        numberOfDays (int): The number of days for which the forecast data is to be extracted.

    Returns:
        JsonResponse: A JSON response containing the weather forecast data.
    """
    # Load XML file and select main element that contains the forecast data
    tree = ET.parse(weatherFileName)
    root = tree.getroot()
    forecast = root.find("*")

    # Populate array with data from XML file
    weatherData = {
        "source": source,
        "lastUpdate": forecast.find("tijd_aanmaak").text,
        "expectation": forecast.find("verwachting_meerdaagse").text,
        "dailyForecast": [],
    }

    # Loop through numberOfDays to populate array with precipitation and temperature for each day
    for index in range(1, numberOfDays + 1):
        dayData = {
            "day": convertDateToRelative(
                forecast.find(f"dag{index}_dddd_dd_mmmm_yyyy").text
            ),
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

    return JsonResponse(weatherData)


def convertDateToRelative(date: str):
    """
    Converts a given date string to a Dutch date description.

    Args:
        date (str): The date string to be converted, formatted as "%A %d %B %Y".

    Returns:
        str: A relative date description in Dutch.
    """
    returnValue = ""

    # Change locale to convert Dutch date from dataset to English
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

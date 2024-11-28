from django.shortcuts import render
import os
from django.http import JsonResponse

# Create your views here.


def createMapsData(request, apiKey, origin, destination, mode):
    mapsData = {
        apiKey: {apiKey},
        origin: {origin},
        destination: {destination},
        mode: {mode},
    }
    return JsonResponse(mapsData)

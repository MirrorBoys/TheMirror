from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # Example data
    widgets = {
        "Weather": 1,
        "Mail": 2,
        "Calendar": 3,
        "News": 4,
        "Clock": 5,
        "ToDoList": 6,
        "Stocks": 7,
        "MusicPlayer": 8,
        "Calculator": 9,
        "Maps": 10,
        "Notes": 11,
        "SocialMedia": 12,
        "FitnessTracker": 13,
        "Photos": 14,
        "WeatherRadar": 15,
        "Games": 16,
    }
    context = {"widgets": widgets}
    return render(request, "theMirror/index.html", context)

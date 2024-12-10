from django.shortcuts import render
from django.http import JsonResponse
from homePage.views import NOTES

# Create your views here.

def fetch_notes(request):
    notes = NOTES
    return JsonResponse(list(notes), safe=False)
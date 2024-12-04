from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def fetch_notes(request):
    notes = "test"
    return JsonResponse(list(notes), safe=False)
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def fetch_notes(request):
    # For the now the data here is hardcoded. Later this will be fetched from the database.
    notes = [
        {
            "title": "test1234",
            "type": "ul",
            "subType": "li",
            "content": [
                "test test test test test test test test test test test test test test test test test test test test test",
                "It can have multiple lines, paragraphs, bulletpoints etc."
            ]
        },
        {
            "title": "test23456789",
            "type": "p",
            "subType": "",
            "content": [
                "hoi",
                "It can have multiple lines, paragraphs, bulletpoints etc."
            ]
        }
    ]
    return JsonResponse(list(notes), safe=False)
from django.shortcuts import render
import os
import requests
from datetime import datetime
from django.http import JsonResponse

# Debug API https://www.googleapis.com/calendar/v3/calendars/s4dsmartmirror@gmail.com/events?key=

# Helper function to format the date-time
def format_datetime(datetime_str):
    try:
        # Fix malformed timezone offset by ensuring it ends with two digits
        if datetime_str[-3] == ":" and len(datetime_str.split(":")[-1]) == 1:
            datetime_str = datetime_str[:-1] + "0"  # Append a zero to fix offset

        # Parse the datetime string with timezone info
        dt_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
        
        # Format the datetime object into a human-readable string
        return dt_obj.strftime('%d %b %Y, %H:%M')  # Example: 28 Nov 2024, 15:15
    except Exception as e:
        print(f"Error formatting datetime: {e} (input: {datetime_str})")
        return datetime_str  # Fallback to the original string if parsing fails

    
# Fetch Google Calendar events
def fetch_google_calendar_events(calendar_id, AGENDA_KEY):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    params = {
        "key": AGENDA_KEY,  # Replace with your actual API key
        "timeMin": datetime.utcnow().isoformat() + "Z",  # Only future events
        "singleEvents": True,  # Expand recurring events
        "orderBy": "startTime",  # Order by start time
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        events = response.json().get("items", [])
        
        # Apply formatting to start and end times
        for event in events:
            if 'dateTime' in event.get('start', {}):
                event['start']['dateTime'] = format_datetime(event['start']['dateTime'])
            if 'dateTime' in event.get('end', {}):
                event['end']['dateTime'] = format_datetime(event['end']['dateTime'])
        
        return events
    else:
        print(f"Error fetching events: {response.status_code}")
        return []

# API endpoint for fetching events
def fetch_agenda_events_view(request):
    calendar_id = "s4dsmartmirror@gmail.com"
    AGENDA_KEY = os.getenv("AGENDA_KEY")
    events = fetch_google_calendar_events(calendar_id, AGENDA_KEY)
    #print(events)  # API Debugging
    return JsonResponse({"events": events})

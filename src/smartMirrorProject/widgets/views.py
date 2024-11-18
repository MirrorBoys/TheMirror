import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .models import Widget

def fetch_time(timezone):
    response = requests.get(f"https://www.timeapi.io/api/time/current/zone?timeZone={timezone}")
    data = response.json()
    date_time_str = data['dateTime'] # Get the date and time string
    date_time_obj = datetime.fromisoformat(date_time_str) # Convert the date and time string to a datetime object
    return f"Timezone: {timezone} " + date_time_obj.strftime('%Y-%m-%d %H:%M:%S') # Return the date and time in a specific format

def widget_grid(request):
    widgets = Widget.objects.all() # Get all widget info from the database
    for widget in widgets:
        if widget.widget_type == 'time':
            widget.content = fetch_time(widget.timezone)
    return render(request, 'widgets/widget_grid.html', {'widgets': widgets}) # Render the widget grid template with the widget info

def update_widgets(request):
    widgets = Widget.objects.all() # Get all widget info from the database
    updated_widgets = [] # Create an empty list to store updated widget info
    for widget in widgets:
        if widget.widget_type == 'time':
            widget.content = fetch_time(widget.timezone)
        updated_widgets.append({ # Append the updated widget info to the list
            'id': widget.id,
            'content': widget.content,
        })
    return JsonResponse({'widgets': updated_widgets}) # Return the updated widget info as a JSON response
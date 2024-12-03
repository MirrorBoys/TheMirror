from datetime import datetime
from django.http import JsonResponse
import pytz

def current_time(request, timezone):
    tz = pytz.timezone(timezone) 
    now = datetime.now(tz)
    current_time = now.strftime("%d-%m-%Y %H:%M:%S")
    return JsonResponse({"current_time": current_time})

# Function to bridge to get timezone from the session (defined in views.py in homePage app) to the time widget
def fetch_session_timezone(request):
    timezone = request.session.get("timezone")
    print(timezone)
    return JsonResponse({"timezone": timezone})
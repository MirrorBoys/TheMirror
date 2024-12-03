from datetime import datetime
from django.http import JsonResponse
import pytz

def current_time(request, timezone):
    decoded_timezone = timezone.replace("-", "/")
    tz = pytz.timezone(decoded_timezone) 
    now = datetime.now(tz)
    current_time = now.strftime("%d-%m-%Y %H:%M")
    return JsonResponse({"current_time": current_time, "timezone": str(tz)})

# Function to get timezone from the session (defined in views.py in homePage app) to the time widget
def fetch_session_timezone(request):
    timezone = request.session.get("timezone")
    encoded_timezone = timezone.replace("/", "-")
    print(encoded_timezone)
    return JsonResponse({"timezone": encoded_timezone})


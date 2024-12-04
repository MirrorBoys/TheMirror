from datetime import datetime
from django.http import JsonResponse
import pytz

def current_time(request, timezone):
    decoded_timezone = timezone.replace("-", "/")
    tz = pytz.timezone(decoded_timezone) 
    now = datetime.now(tz)
    current_time = now.strftime("%d-%m-%Y %H:%M")
    return JsonResponse({"current_time": current_time, "timezone": str(tz)})


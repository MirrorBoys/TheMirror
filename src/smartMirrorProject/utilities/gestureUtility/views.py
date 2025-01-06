from django.http import JsonResponse
from threading import Timer
from . import testscript

# Create your views here.

# Imagine this would be a hand gesture recognition function that would set the global variable gesture to the gesture that was recognized.
gesture = ''

def setGestureData():
    global gesture
    action = None
    if gesture == 'fist':
        action = 'PAUSE'
    elif gesture == 'one':
        action = 'PLAY'
    elif gesture == 'two':
        action = 'SKIP'
    elif gesture == 'l':
        action = 'LOGIN'
    
    return action

def sendGestureData(request):
    gestureData = setGestureData()
    
    response_data = {'gesture': gestureData}
    
    # Reset gesture after sending
    global gesture
    gesture = None
    
    return JsonResponse(response_data)

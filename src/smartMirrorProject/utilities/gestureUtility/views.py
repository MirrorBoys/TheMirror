from django.http import JsonResponse
from threading import Timer
from . import testscript

# Create your views here.

# Imagine this would be a hand gesture recognition function that would set the global variable gesture to the gesture that was recognized.
gesture = ''

def sendGestureData(request):
    gestureData = setGestureData()
    
    response_data = {'gesture': gestureData}
    
    # Reset gesture after sending
    global gesture
    gesture = None
    
    return JsonResponse(response_data)

def setGestureData():
    global gesture
    action = None
    if gesture == is_index_up and are_middle_ring_pinky_down:
        print("Gesture Detected: Index Finger Up!")
        action = 'LOGIN'
    elif gesture == is_middle_up and are_index_ring_pinky_down:
        print("Gesture Detected: You are very rude!!!") 
        action = 'SHUTDOWN'
    elif gesture == are_all_fingers_up:
        print("Gesture Detected: All Fingers Up!")        
        action = 'PAUSE'
    elif gesture == is_my_thumb_up:
        print("Gesture Detected: Like And Subscribe")   
        action = 'PLAY'
    elif gesture == is_pinky_up and is_my_pinky_up:
        print("Gesture Detected: Pinky Up!")    
        action = 'REFRESH'
    elif gesture == is_index_pointing_left:
        print("Gesture Detected: Point Right!")
        action = 'SKIP'
    
    return action

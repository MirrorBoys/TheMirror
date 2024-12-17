from django.http import JsonResponse

# Create your views here.
    
#def gesture(request):
#    ...code for each gesture
#
#    gestureData = None
#
#    if swipeLeft:
#        gestureData = 'LEFT'
#    elif swipeRight:
#        gestureData = 'RIGHT'
#
#    return JsonResponse({'gesture': 'gestureData'})

def math(request):
    gestureData = 'LEFT'
    return JsonResponse({'gesture': gestureData})
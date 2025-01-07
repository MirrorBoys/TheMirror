from django.shortcuts import render


def register(request):

    return render(request, "registrationPage/register.html", {"temp": "temp"})

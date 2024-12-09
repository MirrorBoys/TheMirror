from django.shortcuts import render


def index(request):
    context = {"widgets": None}
    return render(request, "loginPage/index.html", context)

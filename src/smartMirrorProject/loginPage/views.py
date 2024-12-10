from django.shortcuts import render, redirect
from django.contrib.auth import logout


def index(request):
    context = {"widgets": None}
    return render(request, "loginPage/index.html", context)


def userLogout(request):
    logout(request)
    return redirect("loginPageIndex")

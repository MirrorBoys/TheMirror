from django.shortcuts import render, redirect
from django.contrib.auth import logout


def index(request):
    return render(request, "loginPage/index.html")


def userLogout(request):
    logout(request)
    return redirect("loginPageIndex")

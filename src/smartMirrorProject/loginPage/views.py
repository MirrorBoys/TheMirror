from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User


def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        nfc_tag_id = request.POST.get("nfc_tag_id")

        if nfc_tag_id:
            try:
                user = User.objects.get(nfc_tag_id=nfc_tag_id)
                login(request, user)
                return redirect("homePageIndex")
            except User.DoesNotExist:
                form.add_error(None, "Invalid NCF-tag")

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homePageIndex")

    return render(request, "loginPage/index.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("loginPage")

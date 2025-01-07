from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    CustomUserCreationForm is a form for creating new users, extending the built-in UserCreationForm. Needed because we use an custom implementation
    of Django's build-in accounts.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homePageIndex")
    else:
        form = CustomUserCreationForm()
    return render(request, "registrationPage/register.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    nfc_tag_id = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("nfc_tag_id",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nfc_tag_id = self.cleaned_data.get("nfc_tag_id")
        if commit:
            user.save()
        return user


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.nfc_tag_id = request.POST.get("nfc_tag_id")
            user.save()
            login(request, user)
            return redirect("homePageIndex")
    else:
        form = CustomUserCreationForm()
    return render(request, "registrationPage/register.html", {"form": form})

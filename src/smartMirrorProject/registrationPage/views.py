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
            nfc_tag_id = form.cleaned_data.get("nfc_tag_id")

            if User.objects.filter(nfc_tag_id=nfc_tag_id).exists():
                form.add_error(
                    "nfc_tag_id", "A user with this NFC tag ID already exists."
                )
            else:
                # Do not directly save user to enable first adding its NFC tag ID
                user = form.save(commit=False)
                user.nfc_tag_id = nfc_tag_id
                user.save()

                # Login user and redirect to homepage
                login(request, user)
                return redirect("homePageIndex")

        else:
            form.add_error(None, "The entered form is not valid.")

    # Return blank registration form
    else:
        form = CustomUserCreationForm()

    return render(request, "registrationPage/register.html", {"form": form})

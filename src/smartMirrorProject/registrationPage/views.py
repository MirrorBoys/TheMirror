from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
import shutil
from django.conf import settings
import os

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
    """
    Handle user registration.

    This view handles the registration of a new user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page with the form.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            nfc_tag_id = form.cleaned_data.get("nfc_tag_id")

            if User.objects.filter(nfc_tag_id=nfc_tag_id).exists():
                form.add_error(
                    "nfc_tag_id", "A user with this NFC tag ID already exists."
                )
            else:
                username = form.cleaned_data.get("username")
                create_config_file(username, "example_config.yml")

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


def create_config_file(username: str, example_config: str):
    """
    Creates a configuration file for a user by copying an example configuration file.

    Args:
        username (str): The username for which the configuration file is being created.
        example_config (str): The name of the example configuration file to copy.
    """
    config_dir = os.path.join(settings.BASE_DIR, "config")
    example_config_path = os.path.join(config_dir, example_config)

    config_file_name = f"{username}_config.yml"
    config_path = os.path.join(config_dir, config_file_name)

    shutil.copyfile(example_config_path, config_path)

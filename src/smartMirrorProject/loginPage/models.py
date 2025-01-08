from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nfc_tag_id = models.CharField(max_length=255, blank=True, null=True)

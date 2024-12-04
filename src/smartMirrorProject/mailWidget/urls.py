from django.urls import path
from . import views

urlpatterns = [
    path("fetch/", views.fetch_mail_view, name="fetch-mail"),
]
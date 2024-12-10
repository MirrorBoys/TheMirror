from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="loginPageIndex"),
    path("logout/", views.userLogout, name="logout"),
]

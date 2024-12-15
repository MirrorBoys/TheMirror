from django.urls import path
from . import views

urlpatterns = [
    path("fetch", views.fetchNfcTag, name="apiNfcFetch"),
    path("write/<str:password>", views.writeNfcTag, name="apiNfcWrite"),
]

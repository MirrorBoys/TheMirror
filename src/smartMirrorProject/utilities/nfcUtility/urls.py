from django.urls import path
from . import views

urlpatterns = [
    path("fetch/", views.fetchNfcTag, name="apiNfcFetch"),
    path("write/<str:data>", views.writeNfcTag, name="apiNfcWrite"),
    path("isPi/", views.checkIfPi, name="apiNfcCheckIfPi"),
]

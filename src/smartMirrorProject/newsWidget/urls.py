from django.urls import path
from . import views

urlpatterns = [
    path("fetch/<int:numberOfArticles>", views.fetch_news, name="apiNewsFetch"),
]

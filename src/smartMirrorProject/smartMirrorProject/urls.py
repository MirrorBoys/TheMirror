"""
URL configuration for smartMirrorProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homePage.urls")),
    path("", include("registrationPage.urls")),
    path("", include("loginPage.urls")),
    path("api/time/", include("timeWidget.urls")),
    path("musicWidget/", include("musicWidget.urls")),
    path("api/weather/", include("weatherWidget.urls")),
    path("api/news/", include("newsWidget.urls")),
    path("api/travel/", include("travelWidget.urls")),
    path("api/agenda/", include("agendaWidget.urls")),
    path("api/radar/", include("radarWidget.urls")),
    path("api/gesture/", include("utilities.gestureUtility.urls")),
    path("api/note/", include("noteWidget.urls")),
    path("api/nfc/", include("utilities.nfcUtility.urls")),
]

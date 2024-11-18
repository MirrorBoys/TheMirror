from django.urls import path
from .views import widget_grid, update_widgets

urlpatterns = [
    path('', widget_grid, name='widget_grid'),
    path('TheMirror/update-widgets/', update_widgets, name='update_widgets'),
]
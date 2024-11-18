from django.contrib import admin
from .models import Widget

class WidgetAdmin(admin.ModelAdmin):
    # define the fields that will be displayed in the admin panel
    list_display = ('title', 'widget_type', 'city', 'timezone')
    list_filter = ('widget_type',)

# register the model with the admin panel
admin.site.register(Widget, WidgetAdmin)
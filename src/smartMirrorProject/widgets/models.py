from django.db import models

class Widget(models.Model):
    # define the choices for the widget type
    WIDGET_TYPES = [
        ('normal', 'Normal Widget'),
        ('time', 'Time Widget'),
        ('weather', 'Weather Widget'),
    ]
    
    # add a new field to the model
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    widget_type = models.CharField(max_length=10, choices=WIDGET_TYPES, default='normal')
    city = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
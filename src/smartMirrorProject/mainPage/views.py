from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def grid(request):
  template = loader.get_template('mainPage/grid.html')
  return HttpResponse(template.render())
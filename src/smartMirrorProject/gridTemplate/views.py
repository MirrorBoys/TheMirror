from django.shortcuts import HttpResponse, render
from django.template import loader

# Create your views here.

def base(request):
    return render(request, "gridTemplate/base.html", {})

def grid(request):
    return render(request, "gridTemplate/grid.html", {})

def widget(request):
    return render(request, "gridTemplate/widget.html", {})

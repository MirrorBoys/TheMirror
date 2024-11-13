from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def base(response):
  return render(response, "mainPage/base.html", {})

def home(response):
  return render(response, "mainPage/home.html", {})
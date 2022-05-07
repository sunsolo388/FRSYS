from django.db import reset_queries
from django.shortcuts import render

# Create your views here.

def deliver_home(request):
    return render(request,'delivery/homepage.html')

def deliver_glc(request):
    return render(request,'delivery/glc.html')

def deliver_psc(request):
    return render(request,'delivery/psc.html')
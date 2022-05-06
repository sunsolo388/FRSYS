from django.db import reset_queries
from django.shortcuts import render

# Create your views here.

def deliver_home(request):
    return render(request,'delivery/empty.html')
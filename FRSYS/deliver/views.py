from django.db import reset_queries
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect,HttpResponse
from deliver import models
from personnel import models


def deliver_home(request):
    return render(request,'delivery/homepage.html')

def deliver_glc_rwfp(request):
    carinfo=models.Car.objects.all().select_related("staff")
    return render(request,'delivery/glc/glc_rwfp.html',{'carinfo':carinfo})

def deliver_psc_dqrw(request):
    return render(request,'delivery/psc/psc_dqrw.html')

def form(request):
    return render(request,'delivery/form.html')
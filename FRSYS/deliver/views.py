from django.db import reset_queries
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect,HttpResponse
from deliver import models
from personnel.models import Staff


def deliver_home(request):
    return render(request,'delivery/homepage.html')

def deliver_glc_rwfp(request):
    carinfo=models.Car.objects.all().values('car_id','status','cold_chain','load','staff_id')
    staffinfo=Staff.objects.all()
    print(carinfo.filter(status=0))
    context = {
        'freecar': carinfo.filter(status=0),
        'staff': staffinfo,
    }
    return render(request,'delivery/glc/glc_rwfp.html',context=context)

def deliver_psc_dqrw(request):
    return render(request,'delivery/psc/psc_dqrw.html')

def test(request):
    return render(request,'delivery/table.html')
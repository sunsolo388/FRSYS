from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from aftermarket import models
# Create your views here.
#后台管理售后
def AMtable(request):
    if request.method=='GET':
    #跳转到售后表单界面
        return render(request, 'aftermarket/AMtable.html')
    elif request.method=='POST':
        am_id=request.POST.get("AM_id")

        return redirect('aftermarket/?=am_id')

def AMdealing(request,am_id):
    #跳转到处理详情界面
    return render(request,'aftermarket/AMdealing.html')


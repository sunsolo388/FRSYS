from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from aftermarket import models
# Create your views here.
#后台管理售后
def AMtable(request):
    #跳转到售后表单界面
    return render(request, 'aftermarket/AMtableq.html')

def AMdealing(request):
    #跳转到处理详情界面
    return render(request,'aftermarket/AMtable')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from order import models  # 导入models文件

# Create your views here.
def sales_home(request):
    return render(request,'order/empty.html')
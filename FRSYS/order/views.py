from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from order import models  # 导入models文件

# Create your views here.
def sales_home(request):
    return render(request,'order/empty.html')

def sales_order_check(request):
    return render(request,'order/form.html')

def customer_manage(request):
    return render(request,'order/table.html')
    
def order_stats(request):
    return render(request,'order/index.html')

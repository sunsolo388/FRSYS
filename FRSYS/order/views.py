import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'sunsolo_FR.settings')
django.setup()

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from order import models as od # 导入models文件

# Create your views here.
def sales_home(request):
    return render(request,'order/empty.html')


def sales_order_new(request):
    """
    待处理订单
    """
    return render(request,'order/sales/neworder.html')


def sales_order_check(request):
    return render(request,'order/form.html')


def customer_manage(request):
    cus_form = od.Customer.objects.all().order_by('customer_id')
    cus_top_form = od.Customer.objects.all().order_by('-customer_cre')[0:5]
    return render(request,'order/customer/table.html',{'customer_list' : cus_form,'customer_top_list':cus_top_form})


def order_stats(request):
    """
    订单统计
    """
    return render(request,'order/sales/chart.html')


def sales_order_search(request):
    """
    订单查询
    """
    return render(request,'order/sales/search.html')


def sales_order_all(request):
    """
    全部订单
    """
    return render(request,'order/sales/all.html')


def sales_order_correct(request):
    """
    订单修改
    """
    return render(request,'order/sales/form.html')

import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'sunsolo_FR.settings')
django.setup()


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from order import models as od # 导入models文件
from deliver import models as dl
from df_user.models import UserInfo


# Create your views here.
def sales_home(request):
    return render(request,'order/empty.html')


def sales_order_new(request):
    """
    待处理订单
    """
    order_new = od.Order.objects.filter(order_status_id = 1).order_by('-order_time')
    return render(request,'order/sales/neworder.html',{'order_new':order_new})


def customer_manage(request):
    cus_form = UserInfo.objects.all().order_by('id')
    cus_top_form = UserInfo.objects.all().order_by('-ucre')[0:5]
    order_new = od.Order.objects.filter(order_status_id=1)
    #cus_new = od.Customer
    return render(request,'order/customer/table.html',
                  {'customer_list' : cus_form,'customer_top_list':cus_top_form,'order_new':order_new})


def order_stats(request):
    """
    订单统计
    """
    return render(request,'order/sales/chart.html')

"""
def sales_order_search(request):
    if request.method=='GET':
        return render(request,'order/sales/search.html')
    else:
        new_add = request.POST.get('new_address')
"""


def sales_order_all(request):
    """
    全部订单
    """
    orders = od.Order.objects.filter(order_status_id=4).order_by('-order_time')[0:]
    return render(request,'order/sales/all.html',{'orders_list':orders})


def sales_order_correct(request):
    """
    订单修改
    """
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_address = request.POST.get('new_address')  # 采购订单
        try:  # 检查采购订单是否存在
            order = od.Order.objects.get(order_id=order_id)
        except Exception as e:
            order = None
        if order == None:
            messages.add_message(request, messages.ERROR, '不存在该订单号，请检查！')
            return render(request, 'order/sales/form')
        status_id = order.order_status.status_id
        if status_id >= 3:  # 已经发货的时候就不能再修改了
            messages.add_message(request, messages.ERROR, '该订单已经发货，不能修改地址！')
            return render(request, 'order/sales/form')
        else:
            dl.Deliver.objects.filter(deliver_id = order.deliver_id).update(aim_add = new_address)
            messages.add_message(request, messages.SUCCESS, '修改成功！')
            return redirect('order/sales/form')
    return render(request, 'order/sales/form')


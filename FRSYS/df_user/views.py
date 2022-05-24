from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from hashlib import sha1

from .models import GoodsBrowser
from . import user_decorator
from df_order.models import *
from .tasks import *


def register(request):
    context = {
        'title': '用户注册',
    }
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_pwd = request.POST.get('confirm_pwd')
    email = request.POST.get('email')

    # 判断两次密码一致性
    if password != confirm_pwd:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(password.encode('utf8'))
    encrypted_pwd = s1.hexdigest()

    # 创建对象
    UserInfo.objects.create(uname=username, upwd=encrypted_pwd, uemail=email)
    send_active_email(email, username)

    # 注册成功
    context = {
        'title': '用户登陆',
        'username': username,
    }
    return render(request, 'df_user/login.html', context)


def register_exist(request):
    username = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=username).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登陆',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    return render(request, 'df_user/login.html', context)


def login_handle(request):  # 没有利用ajax提交表单
    # 接受请求信息
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    jizhu = request.POST.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:  # 判断用户密码并跳转
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)  # 继承与HttpResponse 在跳转的同时 设置一个cookie值
            # 是否勾选记住用户名，设置cookie
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)  # 设置过期cookie时间，立刻过期
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {
                'title': '用户名登陆',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(request, 'df_user/login.html', context)
    else:
        context = {
            'title': '用户名登陆',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'df_user/login.html', context)


def logout(request):  # 用户登出
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("df_goods:index"))


@user_decorator.login
def info(request):  # 用户中心
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in browser_goods]  # 从浏览商品记录中取出浏览商品
        explain = '最近浏览'
    else:
        explain = '无最近浏览'

    context = {
        'title': '用户中心',
        'page_name': 1,
        'user_phone': user.uphone,
        'user_address': user.uaddress,
        'user_name': username,
        'goods_list': goods_list,
        'explain': explain,
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    context = {
        'paginator': paginator,
        'page': page,
        # 'orders_list':orders_list,
        'title': "用户中心",
        'page_name': 1,
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        user.ushou = request.POST.get('ushou')
        user.uaddress = request.POST.get('uaddress')
        user.uyoubian = request.POST.get('uyoubian')
        user.uphone = request.POST.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': '用户中心',
        'user': user,
    }
    return render(request, 'df_user/user_center_site.html', context)


from django.test import TestCase

# Create your tests here.


''' 溯源功能的实现-后端 '''
from order.models import Order, OrderDetail
from warehouse.models import Inward, WareHouse, Outward
from deliver.models import Deliver, DeliverDetail, CarForDeliver, Car, Staff
from purchase.models import Purchase, PurchaseDetail, Supplier, SupplierDetail


@user_decorator.login
def order_trace(request,index):
    if request.method == 'GET':
        user_id = request.session['user_id']
        orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
        paginator = Paginator(orders_list, 2)
        page = paginator.page(int(index))
        context = {
            'paginator': paginator,
            'page': page,
            # 'orders_list':orders_list,
            'title': "用户中心",
            'page_name': 1,
        }
        ##
        return render(request, 'df_user/user_center_order.html', context)

    elif request.method == 'POST':
        if 'search_order_trace' in request.POST:
            order_id = request.POST.get('order_id')  # 这里看前端到底把这个名字设成啥了

            if order_id:  # 保证有输入内容
                try:
                    # Order实例
                    order = Order.objects.get(order_id=order_id)  # order_time?
                    '''  订单运输过程溯源  '''
                    # Deliver实例
                    deliver_order = order.deliver_id  #
                    car_for_deliver_order = CarForDeliver.objects.get(deliver_id_id=deliver_order.deliver_id)
                    car_order = car_for_deliver_order.car_id  # car_id、cold_chain
                    driver_order = car_order.staff_id  # staff_name
                    # DeliverDetail查询集  这里还需要考虑一个问题，如果这个订单还没发货，从而导致没有DeliverDetail呢
                    deliver_details_order = DeliverDetail.objects.filter(
                        deliver_id_id=deliver_order.deliver_id)  # province、city、detail_time

                    '''  采购过程溯源  '''
                    # OrderDetail查询集
                    order_details = OrderDetail.objects.filter(order_id=order_id)
                    '''  这里的业务逻辑需要沟通  前端需要啥数据 理论上，后端到这儿可以结束了'''

                    for order_detail in order_details:
                        # Outward实例
                        outward = order_detail.outward_id  # out_time
                        # Inward实例
                        inward = outward.warehouse_flow  # in_time
                        ''' 如果还需要Warehouse实例的话，可以用下面这个 不过这个就没办法在前端做到了。后端好像也没法搞'''
                        # 这里获得的是一个WareHouse的查询集，所以我不推荐展示里面的数据
                        # warehouse = WareHouse.objects.filter(warehouse_flow = inward.warehouse_flow)
                        # Purchase实例
                        purchase = inward.purchase_id
                        # PurchaseDetail实例  这里没法在前端完成，所以，还需要进行讨论，该怎么完成
                        purchase_detail = PurchaseDetail.objects.get(
                            purchase_id_id=purchase.purchase_id)  # product_root
                        supplier = purchase_detail.supplier_id  # supplier_name、supplier_add
                        ''' 采购运输过程的溯源 '''
                        # Deliver实例
                        deliver_purchase = purchase.deliver_id
                        car_for_deliver_purchase = CarForDeliver.objects.get(deliver_id_id=deliver_purchase.deliver_id)
                        car_purchase = car_for_deliver_purchase.car_id  # car_id、cold_chain
                        driver_purchase = car_purchase.staff_id  # staff_name
                        # DeliverDetail查询集 这里没法在前端完成，所以，还需要进行讨论，该怎么完成
                        deliver_details_purchase = DeliverDetail.objects.filter(
                            deliver_id_id=deliver_purchase.deliver_id)  # province、city、detail_time

                    '''  溯源过程到此结束  '''

                except Order.DoesNotExist:
                    messages.add_message(request, messages.ERROR, '查询失败！不存在该订单编号！')

    return render(request, 'df_user/findroot.html',locals())# 搞不清现在啥情况,返回哪个页面也不明白。前端来搞

@user_decorator.login
def findroot(request,index):
    return render(request, 'df_user/findroot.html')
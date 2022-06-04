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


''' 溯源功能的实现-后端 '''
from order.models import Order, OrderDetail
from warehouse.models import Inward, WareHouse, Outward
from deliver.models import Deliver, DeliverDetail, CarForDeliver, Car, Staff
from purchase.models import Purchase, PurchaseDetail, Supplier, SupplierDetail
from django.contrib import messages

def _get_trace_info(order_time, car_order, driver_name, deliver_details_order, order_details):
    '''
    trace_info数据说明：
    trace_info包括：
    order_time：一个str形式的time
    car_id：一个str
    cold_chain：一个str
    driver_name：一个str
    deliver_details_order_list：一个列表，列表内的元素是字典，每个字典包括三个键province、city、time
    order_details_info_dic_list：一个列表，列表内的元素是字典，具体如下：
        每个字典包括以下键：
            product_name（对应一个str）、
            purchase(对应一个列表，列表内是字典，具体如下：
                每个字典拥有out_time、in_time、product_root、supplier_name、supplier_add、car_id、cold_chain、driver_name、deliver_details_purchase_list
                    其中deliver_details_purchase_list对应一个列表，列表内的元素是字典，每个字典包括三个键province、city、time
    '''
    # 数据处理准备
    cold_chain_dic={0: '无冷链车辆',
                    1: 'A级冷链冷藏车辆', 2: 'B级冷链冷藏车辆',
                    3: 'C级冷链冷藏车辆', 4: 'D级冷链冷藏车辆',
                    5: 'E级冷链冷藏车辆', 6: 'F级冷链冷藏车辆',
                    7: 'G级冷链冷藏车辆', 8: 'H级冷链冷藏车辆'}
    # 数据处理
    order_time = order_time.strftime('%Y-%m-%d %H:%M:%S')   # 一个str形式的time
    deliver_details_order_list = []                         # 一个列表，列表内的元素是字典，每个字典包括三个键province、city、time
    for deliver_detail_order in deliver_details_order:
        deliver_detail_order_dic = {}
        deliver_detail_order_dic['province'] = deliver_detail_order.province
        deliver_detail_order_dic['city'] = deliver_detail_order.city
        deliver_detail_order_dic['time'] = deliver_detail_order.detail_time.strftime('%Y-%m-%d %H:%M')
        deliver_details_order_list.append(deliver_detail_order_dic)
        
    order_details_info_dic_list = []                                  # 一个列表，列表内的元素是字典，见如下
    for order_detail in order_details:
        product = order_detail.product_id   # product_name
        order_detail_info_dic = {}                           # 一个字典，字典包括以下键：
                                                             # product_name（对应str）、
                                                             # out_time（对应一个列表，列表内是str形式的time)、in_time(对应一个列表,列表内是str形式的time）
                                                             # purchase(对应一个列表，列表内是字典，
                                                                                      # 其中每个字典拥有product_root、supplier_name、supplier_add、car_id、cold_chain、driver_name、deliver_details_purchase_list
                                                                                        # 其中deliver_details_purchase_list对应一个列表，列表内的元素是字典，每个字典每个字典包括三个键province、city、time
        order_detail_info_dic['product_name'] = product.product_name
        outwards = Outward.objects.filter(orderdetail_id=order_detail.order_detail_id)  # out_time
        order_detail_info_dic['purchase'] = []
        for outward in outwards:
            purchase_info_dic = {}
            purchase_info_dic['out_time'] = outward.out_time.strftime('%Y-%m-%d %H:%M:%S')
            inward = outward.warehouse_flow  # in_time
            purchase_info_dic['in_time'] = inward.in_time.strftime('%Y-%m-%d %H:%M:%S')

            purchase = inward.purchase_id
            purchase_detail = PurchaseDetail.objects.get(purchase_id_id=purchase.purchase_id)  # product_root
            purchase_info_dic['product_root'] = purchase_detail.product_root
            supplier = purchase_detail.supplier_id  # supplier_name、supplier_add
            purchase_info_dic['supplier_name'] = supplier.supplier_name
            purchase_info_dic['supplier_add'] = supplier.supplier_add
            ''' 采购运输过程的溯源 '''
            deliver_purchase = purchase.deliver_id
            car_for_deliver_purchase = CarForDeliver.objects.get(deliver_id_id=deliver_purchase.deliver_id)
            car_purchase = car_for_deliver_purchase.car_id  # car_id、cold_chain
            purchase_info_dic['car_id'] = car_purchase.car_id
            purchase_info_dic['cold_chain'] = cold_chain_dic[car_purchase.cold_chain]

            driver_purchase = car_purchase.staff_id  # staff_name
            purchase_info_dic['driver_name'] = driver_purchase.staff_name

            purchase_info_dic['deliver_details_purchase_list'] = [] # 一个列表，列表内的元素是字典，每个字典包括三个键province、city、time
            # DeliverDetail查询集
            deliver_details_purchase = DeliverDetail.objects.filter(deliver_id_id=deliver_purchase.deliver_id)  # province、city、detail_time
            for deliver_detail_purchase in deliver_details_purchase:
                deliver_detail_purchase_dic = {}
                deliver_detail_purchase_dic['province'] = deliver_detail_purchase.province
                deliver_detail_purchase_dic['city'] = deliver_detail_purchase.city
                deliver_detail_purchase_dic['time'] = deliver_detail_purchase.detail_time.strftime('%Y-%m-%d %H:%M')
                purchase_info_dic['deliver_details_purchase_list'].append(deliver_detail_purchase_dic)

            order_detail_info_dic['purchase'].append(purchase_info_dic)

        order_details_info_dic_list.append(order_detail_info_dic)

    return {'order_time':order_time,
            'car_id':car_order.car_id,
            'cold_chain':cold_chain_dic[car_order.cold_chain],
            'driver_name':driver_name,
            'deliver_details_order_list':deliver_details_order_list,
            'order_details_info_dic_list':order_details_info_dic_list
    }
    # 数据展示
'''    print(type(order_time), order_time)
    print(type(car_order.car_id), car_order.car_id)
    print(type(car_order.cold_chain), car_order.cold_chain)
    print(type(driver_name), driver_name)
    for deliver_detail_order_dic in deliver_details_order_list:
        print(type(deliver_detail_order_dic['province']), deliver_detail_order_dic['province'])
        print(type(deliver_detail_order_dic['city']), deliver_detail_order_dic['city'])
        print(type(deliver_detail_order_dic['time']), deliver_detail_order_dic['time'])
    print(order_details_info_dic_list)
    for order_detail_info_dic in order_details_info_dic_list:
        print(type(order_detail_info_dic['product_name']), order_detail_info_dic['product_name'])
        for purchase in order_detail_info_dic['purchase']:
            print(type(purchase['in_time']), purchase['in_time'])
            print(type(purchase['out_time']), purchase['out_time'])
            print(type(purchase['product_root']), purchase['product_root'])
            print(type(purchase['supplier_name']), purchase['supplier_name'])
            print(type(purchase['supplier_add']), purchase['supplier_add'])
            print(type(purchase['car_id']), purchase['car_id'])
            print(type(purchase['cold_chain']), purchase['cold_chain'])
            print(type(purchase['driver_name']), purchase['driver_name'])

            for deliver_detail_purchase_dic in purchase['deliver_details_purchase_list']:
                print(type(deliver_detail_purchase_dic['province']), deliver_detail_purchase_dic['province'])
                print(type(deliver_detail_purchase_dic['city']), deliver_detail_purchase_dic['city'])
                print(type(deliver_detail_purchase_dic['time']), deliver_detail_purchase_dic['time'])
'''


@user_decorator.login
def order_trace(request,index):
    if request.method == 'GET':
        user_id = request.session['user_id']
        orders_list = Order.objects.filter(customer_id=user_id)
        print(orders_list)
        paginator = Paginator(orders_list, 2)
        page = paginator.page(int(index))
        context = {
            'paginator': paginator,
            'page': page,
            'orders_list':orders_list,
            'title': "用户中心",
            'page_name': 1,
        }
        return render(request, 'df_user/user_center_order.html', context)

    elif request.method == 'POST':
        if 'search_order_trace' in request.POST:
            # order_id = '202205281536001'
            order_id = request.POST.get('order_id')  # 这里看前端到底把这个名字设成啥了

            if order_id:  # 保证有输入内容
                try:
                    # Order实例
                    order = Order.objects.get(order_id=order_id)  # order_time
                    '''  订单运输过程溯源  '''
                    # Deliver实例
                   # deliver_order = Deliver.objects.get(order_id=order.deliver_id)  #
                    car_for_deliver_order = CarForDeliver.objects.get(deliver_id_id=order.deliver_id)
                    car_order = car_for_deliver_order.car_id  # car_id、cold_chain
                    driver_order = car_order.staff_id  # staff_name
                    # DeliverDetail查询集  这里还需要考虑一个问题，如果这个订单还没发货，从而导致没有DeliverDetail呢
                    deliver_details_order = DeliverDetail.objects.filter(
                        deliver_id_id=order.deliver_id)  # province、city、detail_time

                    '''  采购过程溯源  '''
                    # OrderDetail查询集
                    order_details = OrderDetail.objects.filter(order_id_id=order_id)

                    trace_info = _get_trace_info(order.order_time,car_order,driver_order.staff_name,deliver_details_order,order_details)
                   # print(trace_info)  # 如果你想看看数据到底啥样，可以取消该注释看看，不过，你没有数据，所以大概率看不到啥。

                except Order.DoesNotExist:
                    messages.add_message(request, messages.ERROR, '查询失败！不存在该订单编号！')
                except CarForDeliver.DoesNotExist:
                    messages.add_message(request, messages.ERROR, '查询失败！订单还未发货！')
                    user_id = request.session['user_id']

                    return redirect('/user/order/'+str(user_id))

                return render(request, 'df_user/findroot.html', locals())

        elif 'aftermarket' in request.POST:
                # order_id = request.POST.get('order_id')

                order_id = request.POST.get('order_id')
                return render(request, 'df_user/user_center_aftermarket_register.html',locals())




@user_decorator.login
def findroot(request,index):
    return render(request, 'df_user/findroot.html')

from aftermarket import models as amm

@user_decorator.login
def aftermarket(request):
    if request.method=='GET':

        return render(request, 'df_user/user_center_aftermarket_register.html')
    else:
            if 'aftermarket' in request.POST:
                m_s=0
                order_id=request.POST.get("order_id")
                order = Order.objects.get(order_id = order_id)
                reason=request.POST.get('reason')
                detail=request.POST.get("detail_info")
                AM_id="am"+order_id
                AM_status='未处理'

                AM=amm.AM.objects.create(AM_id=AM_id,order_id=order,reason_kind=reason,reason_detail=detail,AM_status=AM_status)
                m_s=1
                if m_s==1:
                    messages.error(request, '申请成功，请等待审核！')

                return redirect("/user/order/1")

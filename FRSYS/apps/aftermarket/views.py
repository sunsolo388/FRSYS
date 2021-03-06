from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from aftermarket import models as amm
from order.models import Order
import os
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from df_user import user_decorator


@user_decorator.worker
def AMtable(request):
    # 跳转到售后表单界面
    if request.method == 'GET':
        try:
            aminfo = amm.AM.objects.all()
        except Exception as e:
            aminfo = None
        # 此处可以留作扩展显示未查询到有处理信息怎么办
        return render(request, 'aftermarket/AMtable.html', locals())
    else:
            am_id = request.POST.get("am_id")

            return redirect(AMdealing, am_id=am_id)

@user_decorator.worker
def AMdealing(request, am_id):
    # 跳转到处理详情界面

    if request.method == 'GET':
        AMID = am_id
        aminfo = amm.AM.objects.all()
        orderID = None
        reasontype = None
        AMdetails = None
        for i in aminfo:
            if i.AM_id == AMID:
                orderID = i.order_id
                reasontype = i.reason_kind
                AMdetails = i.reason_detail
        return render(request, 'aftermarket/AMdealing.html', locals())

    else:

        if 'dealing submit' in request.POST:
            dealingtext = request.POST.get('dealtext')
            dealresult = request.POST.get('optionsRadios')
            if dealresult == 0:
                dealresult = '退款'
            elif dealresult == 1:
                dealresult = '不予退款'
            amevent = amm.AM.objects.get(AM_id=am_id)
            order_id = amevent.order_id

            dealing_AM = amm.AM_feedback.objects.create(order_id=order_id,dealingtxt=dealingtext,dealing_result=dealresult)
            amevent.AM_status = '已处理'
            amevent.save()

        return redirect('/work/aftermarket')


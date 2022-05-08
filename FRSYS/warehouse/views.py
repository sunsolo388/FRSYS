from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from warehouse import models as wm # 导入models文件
from purchase import models as pm  #导入purchase检查采购订单编号
from login import models as lm     #导入login检查是否存在该员工

def warehouse_home(request):
    '''
    仓库主页
    '''
    return render(request,'warehouse/index.html')

def warehouse_inward(request):
    '''
    入库管理
    '''
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')       #采购订单
        warehouse_flow = request.POST.get('warehouse_flow') #仓库流水
      #  password = request.POST.get('password')             #提交的时候要输入账号密码
      #  email = request.POST.get('email')
        product = request.POST.get('identity')          #商品种类
        date = request.POST.get('time')                 #时间
        print(date)
        in_num = request.POST.get('in_num')             #入库质量

        try:                                            #检查采购订单是否存在，是不是乱输的
            purchase = pm.Purchase.objects.get(purchase_id=purchase_id)
           # print(purchase)
        except Exception as e:
            purchase = None
        if purchase == None:
            messages.add_message(request, messages.ERROR, '不存在该订单号，请检查！')
            return render(request, 'warehouse/inward.html')
        try:
            purchase_already = wm.Inward.objects.get(purchase_id=purchase_id)
            warehouse_flow_already = wm.Inward.objects.get(warehouse_flow=warehouse_flow)
        except Exception as e:
            purchase_already = None
            warehouse_flow_already = None
        if purchase_already != None:
            messages.add_message(request, messages.ERROR, '重复的订单号，请重新输入！')
            return render(request, 'warehouse/inward.html')
        elif warehouse_flow_already != None:
            messages.add_message(request, messages.ERROR, '重复的流水号，请重新输入！')
            return render(request, 'warehouse/inward.html')
        else:
        # 将数据保存到数据库
            wm.Inward.objects.create(
                purchase_id=purchase, in_time=date,
                warehouse_flow=warehouse_flow, in_num=in_num, product_name=product
            )
            messages.add_message(request, messages.SUCCESS, '添加成功！')
            return redirect('/work/warehouse/inward')
    return render(request,'warehouse/inward.html')
def warehouse_outward(request):
    '''
    出库管理
    '''
    return render(request,'warehouse/outward.html')
"""
def test(request):
    return render(request,'delivery/tab-panel.html')
"""

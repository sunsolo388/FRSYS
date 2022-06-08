from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models.aggregates import Sum
from warehouse import models as wm # 导入models文件
from purchase import models as pm  #导入purchase检查采购订单编号
from login import models as lm     #导入login检查是否存在该员工
from order import models as om
from product import models as pdm
from df_goods import models as gm
from itertools import chain

import os
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from df_user import user_decorator


productinfo = pdm.Product.objects.all().values('product_name','product_id')
pdc = productinfo

@user_decorator.worker
def warehouse_home(request):
    '''
    仓库主页
    '''
    totalfruit = gm.GoodsInfo.objects.filter(gtype__ttitle='新鲜水果').aggregate(num=Sum('gkucun'))
    fruit = totalfruit['num']  # 计算当前水果总库存
    if fruit == None:
        fruit = 0
    totalseafood = gm.GoodsInfo.objects.filter(gtype__ttitle='海鲜水产').aggregate(num=Sum('gkucun'))
    seafood = totalseafood['num']  # 计算当前海鲜总库存
    if seafood == None:
        seafood = 0
    totalmeat = gm.GoodsInfo.objects.filter(gtype__ttitle='牛羊猪肉').aggregate(num=Sum('gkucun'))
    meat = totalmeat['num']  # 计算当前肉类总库存
    if meat == None:
        meat = 0
    totaleggs = gm.GoodsInfo.objects.filter(gtype__ttitle='禽类蛋品').aggregate(num=Sum('gkucun'))
    eggs = totaleggs['num']  # 计算当前蛋类总库存
    if eggs == None:
        eggs = 0
    totalvege = gm.GoodsInfo.objects.filter(gtype__ttitle='新鲜蔬菜').aggregate(num=Sum('gkucun'))
    vegetable = totalvege['num']  # 计算当前蔬菜总库存
    if vegetable == None :
        vegetable = 0
    totalfrozen = gm.GoodsInfo.objects.filter(gtype__ttitle='速冻食品').aggregate(num=Sum('gkucun'))
    frozen = totalfrozen['num']  # 计算当前水果总库存
    if frozen == None:
        frozen = 0

    leftinfo = {'fruit':fruit//100,'seafood':seafood//100,'meat':int(meat)//100,
                'eggs':int(eggs)//100,'vegetable':int(vegetable)//100,'frozen':int(frozen)//100}

    warehouseinfo = wm.WareHouse.objects.all().values(
        'warehouse_flow', 'product_name', 'left_num', 'warehouse_status'
    )
    kcxx = warehouseinfo


    context = {'kcxx': kcxx,'pdc':pdc,'left':leftinfo}
    if request.method == 'POST':
        num = request.POST.get('num')
        time = request.POST.get('time')
        product = request.POST.get('identity')
        product_id = pdm.Product.objects.filter(product_name = product).first()
        pdm.PurchaseDemand.objects.create(
            product_id = product_id, pdemand_num = num,
            pdemand_time = time
        )
        messages.add_message(request, messages.SUCCESS, '申请成功！')
        return redirect('/work/warehouse')

    return render(request,'warehouse/index.html',context=context)

@user_decorator.worker
def warehouse_inward(request):
    '''
    入库管理
    '''
    purchase_already = wm.Inward.objects.all()
    purchase_to_choose = pm.Purchase.objects.exclude(purchase_id__in = purchase_already)
    #purchaseinfo = purchase_to_choose.values('purchase_id','purchase_num')
    pinfo = pm.PurchaseDetail.objects.filter(purchase_id__in = purchase_to_choose).values(
        'purchase_id','product_id__product_name','purchase_id__purchase_num')


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
            warehouse_flow1 = wm.Inward.objects.filter(purchase_id=purchase_id).first()
            wm.WareHouse.objects.create(
                warehouse_flow=warehouse_flow1,left_num = in_num,product_name = product,
                warehouse_status = '库存'
            )

            total = wm.WareHouse.objects.filter(product_name=product, warehouse_status='库存').aggregate(num=Sum('left_num'))
            total_num = total['num']  # 计算当前该产品剩余总库存
            gm.GoodsInfo.objects.filter(gtitle=product).update(gkucun=total_num * 2)

            messages.add_message(request, messages.SUCCESS, '添加成功！')
            return redirect('/work/warehouse/inward')

    inwardinfo = wm.Inward.objects.all().order_by('in_time').values(
    'purchase_id','warehouse_flow','product_name','in_num','in_time'
    )
    rkxx = inwardinfo
    context = {'rkxx':rkxx,'pdc':pdc,'pinfo':pinfo}
    return render(request,'warehouse/inward.html',context=context)


@user_decorator.worker
def warehouse_outward(request):
    '''
    出库管理
    '''
    order_to_complete = om.Order.objects.filter(order_status=1)
    orderinfo = om.OrderDetail.objects.filter(order_id__in=order_to_complete).values(
        'order_detail_id', 'product_id__product_name', 'detail_num','order_detail_status'
    )  # 筛选出所有未处理的orderDetail
    xsdd = orderinfo

    #进入出库界面就删掉多余的库存信息
    try:
        to_delete = wm.WareHouse.objects.get(left_num=0)
        to_delete.delete()
    except:
        print('没有数据需要删除')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')  # 销售详情编号
        outward_id = request.POST.get('outward_id')  # 出库编号
        product = request.POST.get('identity')  # 商品种类
        date = request.POST.get('time')  # 时间
      #  print(date)
        out_num = int(request.POST.get('out_num'))  # 出库质量
        try:  # 检查销售订单是否存在，是不是乱输的
            order = om.OrderDetail.objects.get(order_detail_id=order_id)
        # print(purchase)
        except Exception as e:
            order = None
        if order == None:
            messages.add_message(request, messages.ERROR, '不存在该订单号，请检查！')
            return render(request, 'warehouse/outward.html')

        total = wm.WareHouse.objects.filter(product_name=product,warehouse_status='库存').aggregate(nums=Sum('left_num'))
        total_num = total['nums']        #计算该产品剩余总库存
       # print(type(total))        #需要调整一下
       # total_num = wm.WareHouse.objects.values('left_num').annotate(num=Sum('left_num')).filter(product_name=product,warehouse_status='库存')
       # print(total_num)
        if total_num == None:
            total_num = 0
        if out_num > total_num:
            messages.add_message(request, messages.ERROR, '库存不足，请补货！')
            return render(request, 'warehouse/index.html')
        # 分配仓库流水和出库商品
        temp_num = 0
        i = 0
        while out_num > temp_num:                                                                               #如果不够就找下一个流水
            warehouse = wm.WareHouse.objects.all().order_by('warehouse_flow__in_time').filter(product_name=product,warehouse_status='库存').values(
                'warehouse_flow', 'left_num')  # 返回字典
            warehouse_flow = warehouse[i]['warehouse_flow']  # 从入库最早的开始,返回一个仓库流水
            # print(warehouse_flow['warehouse_flow'])
            # warehouse_flow1 = wm.Inward.objects.filter(warehouse_flow=warehouse_flow).first()                       #返回该流水对应的入库实例
            temp_num = warehouse[i]['left_num']  # 在库存里找货
            origin_num = warehouse[i]['left_num'] #原始库存
            if out_num <= temp_num:
                temp_num = out_num
            out_num -= temp_num
            warehouse_flow1 = wm.Inward.objects.filter(warehouse_flow=warehouse_flow).first()  # 返回该流水对应的入库实例
            # 修改库存信息
            try:
                wm.WareHouse.objects.create(
                    warehouse_flow = warehouse_flow1,left_num = temp_num,
                    warehouse_status = '出库',product_name = product
                )
            except Exception:
                wm.WareHouse.objects.filter(
                    warehouse_flow=warehouse_flow1,
                    warehouse_status='出库', product_name=product
                ).update(left_num=temp_num)



            wm.WareHouse.objects.filter(warehouse_flow=warehouse_flow1,warehouse_status='库存').update(
                left_num=origin_num-temp_num
            )
            #修改出库表
            outward_id1 = outward_id+f'_{i}'
            wm.Outward.objects.create(
                outward_id = outward_id1,
                orderdetail_id = order_id,
                warehouse_flow = warehouse_flow1,
                out_num = temp_num,
                out_time = date,
                product_name = product
            )
            if out_num > 0:
                i+=1
                temp_num = 0

        total = wm.WareHouse.objects.filter(product_name=product, warehouse_status='库存').aggregate(num=Sum('left_num'))
        total_num = total['num']  # 计算当前该产品剩余总库存
        gm.GoodsInfo.objects.filter(gtitle=product).update(gkucun=total_num * 2)
        order = om.OrderDetail.objects.filter(order_detail_id=order_id).values('order_id')[0]['order_id']
        om.OrderDetail.objects.filter(order_detail_id=order_id).update(order_detail_status=1)
        ordertotal = om.OrderDetail.objects.filter(order_id=order).values('order_detail_status')
        flag = 1
        for i in range(len(ordertotal)):
            if ordertotal[i]['order_detail_status'] == False:
                flag = 0
        if flag == 1:
            om.Order.objects.filter(order_id=order).update(order_status=2)  # 更新order表
        messages.add_message(request, messages.SUCCESS, '添加成功！')
        return redirect('/work/warehouse/outward')

    outwardinfo = wm.Outward.objects.all().order_by('out_time').values(
        'outward_id', 'warehouse_flow', 'product_name',
        'out_time','out_num'
    )
    ckxx = outwardinfo

    context = {'ckxx': ckxx,'pdc':pdc,'xsdd':xsdd}
    return render(request, 'warehouse/outward.html', context=context)

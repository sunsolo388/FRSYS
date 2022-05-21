from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from warehouse import models as wm # 导入models文件
from purchase import models as pm  #导入purchase检查采购订单编号
from login import models as lm     #导入login检查是否存在该员工
from order import models as om
from product import models as pdm

productinfo = pdm.Product.objects.all().values('product_name','product_id')
pdc = productinfo
def warehouse_home(request):
    '''
    仓库主页
    '''
    warehouseinfo = wm.WareHouse.objects.all().values(
        'warehouse_flow', 'product_name', 'left_num', 'warehouse_status'
    )
    kcxx = warehouseinfo

    context = {'kcxx': kcxx,'pdc':pdc}
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
            warehouse_flow1 = wm.Inward.objects.filter(purchase_id=purchase_id).first()
            wm.WareHouse.objects.create(
                warehouse_flow=warehouse_flow1,left_num = in_num,product_name = product,
                warehouse_status = '库存'
            )
            messages.add_message(request, messages.SUCCESS, '添加成功！')
            return redirect('/work/warehouse/inward')

    inwardinfo = wm.Inward.objects.all().order_by('in_time').values(
    'purchase_id','warehouse_flow','product_name','in_num','in_time'
    )
    rkxx = inwardinfo
    context = {'rkxx':rkxx,'pdc':pdc}
   # print('哈哈哈哈')
   # print('xxxxxxxxx' +str(context))
    return render(request,'warehouse/inward.html',context=context)



def warehouse_outward(request):
    '''
    出库管理
    '''
    if request.method == 'POST':
        order_id = request.POST.get('order_id')  # 销售订单
        outward_id = request.POST.get('outward_id')  # 出库编号
        product = request.POST.get('identity')  # 商品种类
        date = request.POST.get('time')  # 时间
      #  print(date)
        out_num = int(request.POST.get('out_num'))  # 出库质量
        try:  # 检查销售订单是否存在，是不是乱输的
            order = om.Order.objects.get(order_id=order_id)
        # print(purchase)
        except Exception as e:
            order = None
        if order == None:
            messages.add_message(request, messages.ERROR, '不存在该订单号，请检查！')
            return render(request, 'warehouse/outward.html')

        #分配仓库流水和出库商品
        temp_num = 0
        while out_num > temp_num:                                                                               #如果不够就找下一个流水
            i=0
            warehouse = wm.WareHouse.objects.all().order_by('warehouse_flow__in_time').filter(product_name=product,warehouse_status='库存').values(
                'warehouse_flow', 'left_num')  # 返回字典
            warehouse_flow = warehouse[i]['warehouse_flow']  # 从入库最早的开始,返回一个仓库流水
            # print(warehouse_flow['warehouse_flow'])
            # warehouse_flow1 = wm.Inward.objects.filter(warehouse_flow=warehouse_flow).first()                       #返回该流水对应的入库实例
            temp_num = warehouse[i]['left_num']  # 在库存里找货
            origin_num = warehouse[i]['left_num'] #原始库存
            if out_num <= temp_num:
                temp_num = out_num
            else:
                out_num -= temp_num
                i+=1
            warehouse_flow1 = wm.Inward.objects.filter(warehouse_flow=warehouse_flow).first()  # 返回该流水对应的入库实例
            # 修改库存信息
            #在order中添加出库时间，更改库存信息：出库的商品改为出库，同一批未完全出售的商品质量减少
          #  om.Order.objects.filter(order_id = order_id).update(out_time=date,warehouse_flow=warehouse_flow)
            wm.WareHouse.objects.create(
                warehouse_flow = warehouse_flow1,left_num = temp_num,
                warehouse_status = '出库',product_name = product
            )
            wm.WareHouse.objects.filter(warehouse_flow=warehouse_flow1,warehouse_status='库存').update(
                left_num=origin_num-temp_num
            )
            #修改出库表
            outward_id = outward_id+f'_{i}'
            wm.Outward.objects.create(
                outward_id = outward_id,
                warehouse_flow = warehouse_flow1,
                out_num = temp_num,
                out_time = date,
                product_name = product
            )

        messages.add_message(request, messages.SUCCESS, '添加成功！')
        return redirect('/work/warehouse/outward')
    outwardinfo = wm.Outward.objects.all().order_by('out_time').values(
        'outward_id', 'warehouse_flow', 'product_name',
        'out_time','out_num'           #这个地方应该要修改
    )
    ckxx = outwardinfo
    context = {'ckxx': ckxx,'pdc':pdc}
    # print('哈哈哈哈')
    # print('xxxxxxxxx' +str(context))
    return render(request, 'warehouse/outward.html', context=context)



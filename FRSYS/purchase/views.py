import django
from django.db import reset_queries
from django.shortcuts import redirect, render, reverse
from django.shortcuts import HttpResponseRedirect,HttpResponse
from sympy import det, re
from django.contrib import messages
from purchase import models
from product.models import PurchaseDemand

# Create your views here.
# 采购部主页
def purchase_home(request):
    return render(request,'purchase/homepage.html')



def get_supplier_info(supplier):
    return {'supplier_id':supplier.supplier_id,
         'supplier_name':supplier.supplier_name,
         'supplier_add':supplier.supplier_add,
         'supplier_charge_name':supplier.supplier_charge_name,
         'supplier_charge_phone': supplier.supplier_charge_phone
         }
# 管理供应商信息
def purchase_manage_suppliers_info(request):
    _content = 0
    suppliers_info = models.Supplier.objects.all().order_by('supplier_id').values(
        'supplier_id','supplier_name','supplier_add',
        'supplier_charge_name','supplier_charge_phone'
    )
    # 这里是初始化页面展示时，可以设置为展示后台所有的供应商，也可以设置为不展示内容
    context = {'suppliers_info':None}

    if request.method=='POST':
        # 查询功能
        if 'search_supplier' in request.POST:
            supplier_id = request.POST.get("supplier_id")
            supplier_name = request.POST.get("supplier_name")
            supplier_add = request.POST.get("supplier_add")
            supplier_charge_name = request.POST.get("supplier_charge_name")
            supplier_charge_phone = request.POST.get("supplier_charge_phone")

            if supplier_id:
                suppliers_info = suppliers_info.filter(supplier_id__icontains = supplier_id)
                _content = 1
            if supplier_name:
                suppliers_info = suppliers_info.filter(supplier_name__icontains = supplier_name)
                _content = 1
            if supplier_add :
                suppliers_info = suppliers_info.filter(supplier_add__icontains = supplier_add )
                _content = 1
            if supplier_charge_name:
                suppliers_info = suppliers_info.filter(supplier_charge_name__icontains = supplier_charge_name)
                _content = 1
            if supplier_charge_phone:
                suppliers_info = suppliers_info.filter(supplier_charge_phone = supplier_charge_phone)
                _content = 1

            if _content:    context['suppliers_info'] = suppliers_info

        # 编辑功能
        elif 'update_supplier' in request.POST:
            supplier_id = request.POST.get('table_supplier_id')
            supplier = models.Supplier.objects.get(supplier_id=supplier_id)
            # 这里可以写一个函数来处理supplier的信息
            request.session['table_supplier'] = get_supplier_info(supplier)
            return redirect('/work/purchase/manage_supplierinfo/update/')
        # 删除功能
        elif 'delete_supplier' in request.POST:
            supplier_id = request.POST.get('table_supplier_id')
            supplier= models.Supplier.objects.get(supplier_id=supplier_id)
            # 修改采购需求状态
            supplier.delete()

            return redirect('/work/purchase/manage_supplierinfo/')

    return render(request,'purchase/manage_supplierinfo/homepage.html',context=context)

## 添加供应商信息
def purchase_manage_supplierinfo_add_info(request):
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name')
        supplier_add = request.POST.get('supplier_add')
        supplier_charge_name = request.POST.get('supplier_charge_name')
        supplier_charge_phone = request.POST.get('supplier_charge_phone')
        try:
            new_supplier = models.Supplier.add_supplier(supplier_add,supplier_charge_phone,supplier_name,supplier_charge_name)

            messages.add_message(request, messages.SUCCESS, '添加成功！')
            return HttpResponseRedirect(reverse('add_supplier'))
        except ValueError:
            messages.add_message(request, messages.ERROR, '添加失败，已存在该供应商信息！')
            return HttpResponseRedirect(reverse('add_supplier'))
    else:
        return render(request,'purchase/manage_supplierinfo/add.html')

## 更新供应商信息
def purchase_manage_supplierinfo_update_info(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        supplier_name = request.POST.get('supplier_name')
        supplier_add = request.POST.get('supplier_add')
        supplier_charge_name = request.POST.get('supplier_charge_name')
        supplier_charge_phone = request.POST.get('supplier_charge_phone')
        try:
            supplier = models.Supplier.objects.get(supplier_id=supplier_id)
            supplier.update_supplier(supplier_id=supplier_id, supplier_name=supplier_name, supplier_add=supplier_add,
                                    supplier_charge_phone=supplier_charge_phone, supplier_charge_name=supplier_charge_name)

            messages.add_message(request, messages.SUCCESS, '更新成功！')
            request.session["table_supplier"] = None
            return HttpResponseRedirect(reverse('update_supplier'))
        except models.Supplier.DoesNotExist:
            messages.error(request, '更新失败! 请检查供应商编号是否输入错误！')
            return HttpResponseRedirect(reverse('update_supplier'))
        except ValueError as ve:
            messages.error(request, ve)
            return HttpResponseRedirect(reverse('update_supplier'))
    else:
        return render(request, 'purchase/manage_supplierinfo/update.html')



def get_purchase_order_info(purchase_detail):
    return {'purchase_id' : purchase_detail.purchase_id.purchase_id,
            'purchase_time': purchase_detail.purchase_id.purchase_time.strftime('%Y-%m-%d'),
            'purchase_num' : purchase_detail.purchase_id.purchase_num,
            'purchase_price': purchase_detail.purchase_id.purchase_price,
            'product_name' : purchase_detail.product_id.product_name,
            'product_type' : purchase_detail.product_id.product_type,
            'supplier_name' : purchase_detail.supplier_id.supplier_name,
            'product_root' : purchase_detail.product_root
            }
# 制定采购决策
def purchase_make_purchases(request):
    purchase_detail = models.PurchaseDetail.objects.all()

    _content = 0
    context = {'purchase_orders_info': None}

    if request.method=='POST':
        # 查询功能
        if 'search_purchase_order' in request.POST:
            purchase_id = request.POST.get('purchase_id')
            product_name = request.POST.get('product_name')
            supplier_name = request.POST.get('supplier_name')
            purchase_time = request.POST.get('purchase_time')

            if purchase_id:
                purchase_detail = purchase_detail.filter(purchase_id = purchase_id)
                _content = 1
            if product_name:    # 如果商品名称不为空，那么搜索相关商品的采购订单
                product = models.Product.objects.filter(product_name__icontains = product_name)    # 首先搜索包含该名称的所有商品
                if product:   # 保证在有搜索到商品的情况下进行   避免报错
                    p = product[0]  # 先更新为搜索出的第一个商品对应的所有订单详情
                    new_purchase_detail = purchase_detail.filter(product_id_id = p.product_id)
                    for p in product[1:]:   # 如果搜索到的商品不止一个，那么将后续的商品对应的所有订单详情并入purchase_detail
                        new_purchase_detail = new_purchase_detail | purchase_detail.filter(product_id_id = p.product_id)
                    # 对purchase_detail进行更新
                    ''' 这里是采用union的方法，会报错，不推荐使用
                    print('new_purchase_detail:')
                    for pd in new_purchase_detail:
                        print(pd.purchase_id)
                    print('purchase_detail:')
                    for pd in purchase_detail:
                        print(pd.purchase_id)
                    purchase_detail = purchase_detail & new_purchase_detail
                    '''
                    purchase_detail = new_purchase_detail.distinct()
                else:
                    purchase_detail = None
                _content = 1
            if supplier_name:   # 这里的处理过程和商品名称的处理过程基本一致
                supplier = models.Supplier.objects.filter(supplier_name__icontains = supplier_name)
                if supplier:
                    s = supplier[0]
                    new_purchase_detail = purchase_detail.filter(supplier_id_id = s.supplier_id)
                    for s in supplier[1:]:
                        new_purchase_detail = new_purchase_detail | purchase_detail.filter(supplier_id_id = s.supplier_id)
                    # 对purchase_detail进行更新
                    purchase_detail = new_purchase_detail.distinct()
                else:
                    purchase_detail = None
                _content = 1
            if purchase_time:
                purchase = models.Purchase.objects.filter(purchase_time = purchase_time)
                if purchase:
                    p = purchase[0]
                    new_purchase_detail = purchase_detail.filter(purchase_id_id = p.purchase_id)
                    for p in purchase[1:]:
                        new_purchase_detail = new_purchase_detail | purchase_detail.filter(purchase_id_id=p.purchase_id)
                    # 对purchase_detail进行更新
                    purchase_detail = new_purchase_detail.distinct()
                else:
                    purchase_detail = None
                _content = 1

            if _content:    context['purchase_orders_info'] = purchase_detail
        # 编辑功能
        elif 'update_purchase_order' in request.POST:
            purchase_id = request.POST.get('table_purchase_id')
            purchase_detail = models.PurchaseDetail.objects.get(purchase_id_id =purchase_id)
            request.session['table_purchase_order'] = get_purchase_order_info(purchase_detail)
            return redirect('/work/purchase/make_purchase/update/')
        # 删除功能
        elif 'delete_purchase_order' in request.POST:
            purchase_id = request.POST.get('table_purchase_id')
            purchase_detail = models.PurchaseDetail.objects.get(purchase_id_id =purchase_id)
            # 修改采购需求状态
            purchase_detail.delete()

            return redirect('/work/purchase/make_purchase/')

    return render(request,'purchase/make_purchase/homepage.html',context=context)

## 添加采购订单
def purchase_make_purchase_add_purchase(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_type = request.POST.get('product_type')
        purchase_num = request.POST.get('purchase_num')
        supplier_name = request.POST.get('supplier_name')
        purchase_time = request.POST.get('purchase_time')
        purchase_price = request.POST.get('purchase_price')
        product_root = request.POST.get('product_root')

        try:
            new_purchase_oder = models.Purchase.add_purchase_order(purchase_num=purchase_num, purchase_time=purchase_time,
                                                               purchase_price=purchase_price, supplier_name=supplier_name,
                                                               product_name=product_name, product_type=product_type,
                                                               product_root=product_root)

            messages.add_message(request, messages.SUCCESS, '添加成功！')
            return HttpResponseRedirect(reverse('add_purchase'))

        except ValueError as ve:
            messages.add_message(request, messages.ERROR, ve)
            return HttpResponseRedirect(reverse('add_purchase'))

    else:
        return render(request,'purchase/make_purchase/add.html')

## 更新采购订单信息
def purchase_make_purchase_update_purchase(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        product_name = request.POST.get('product_name')
        product_type = request.POST.get('product_type')
        purchase_num = request.POST.get('purchase_num')
        supplier_name = request.POST.get('supplier_name')
        purchase_time = request.POST.get('purchase_time')
        purchase_price = request.POST.get('purchase_price')
        product_root = request.POST.get('product_root')

        try:
            models.Purchase.update_purchase_order(purchase_id=purchase_id,purchase_num=purchase_num,
                                                     purchase_time=purchase_time, purchase_price=purchase_price,
                                                     supplier_name=supplier_name, product_name=product_name,
                                                     product_type=product_type, product_root=product_root)

            messages.add_message(request, messages.SUCCESS, '更新成功！')
            request.session["table_purchase_order"] = None
            return HttpResponseRedirect(reverse('update_purchase'))
        except ValueError as ve:
            messages.add_message(request, messages.ERROR, ve)
            return HttpResponseRedirect(reverse('update_purchase'))

    else:
        return render(request,'purchase/make_purchase/update.html')



# 采购需求管理
# 查看采购需求
def purchase_purchase_demands(request):
    purchase_demand = PurchaseDemand.objects.all()
    _content = 0
    context = {'purchase_demand_info':None}

    if request.method == 'POST':
        if 'search_purchase_demand' in request.POST:
            pdemand_time = request.POST.get('pdemand_time')
            product_name = request.POST.get('product_name')
            product_type = request.POST.get('product_type')
            pdemand_state = request.POST.get('pdemand_state')

            if pdemand_time:
                purchase_demand = purchase_demand.filter(pdemand_time = pdemand_time)
                _content = 1
            if pdemand_state != '':
                # 由于获取到的是“未完成”和“已完成”,故需要先进行转换
                if pdemand_state == '未完成需求':  pdemand_state = 0
                elif pdemand_state == '已完成需求': pdemand_state = 1
                purchase_demand = purchase_demand.filter(pdemand_state = pdemand_state)
                _content = 1
            if product_name:    # 类似于采购订单的处理
                product = models.Product.objects.filter(product_name__icontains=product_name)  # 首先搜索包含该名称的所有商品
                if product:
                    p = product[0]
                    new_purchase_demand = purchase_demand.filter(product_id_id=p.product_id)
                    for p in product[1:]:
                        new_purchase_demand = new_purchase_demand | purchase_demand.filter(product_id_id=p.product_id)
                    purchase_demand = new_purchase_demand.distinct()
                else:
                    purchase_demand = None
                _content = 1
            if product_type:
                product = models.Product.objects.filter(product_type__icontains=product_type)
                if product:
                    p = product[0]
                    new_purchase_demand = purchase_demand.filter(product_id_id=p.product_id)
                    for p in product[1:]:
                        new_purchase_demand = new_purchase_demand | purchase_demand.filter(product_id_id=p.product_id)
                    purchase_demand = new_purchase_demand.distinct()
                else:
                    purchase_demand = None
                _content = 1

            if _content:    context['purchase_demand_info'] = purchase_demand
        elif 'update_purchase_demand_state' in request.POST:
            purchase_demand_id = request.POST.get('table_purchase_demand_id')
            purchase_demand = PurchaseDemand.objects.get(pdemand_id=purchase_demand_id)
            # 修改采购需求状态 可优化
            if purchase_demand.pdemand_state:
                purchase_demand.pdemand_state = 0
            else:
                purchase_demand.pdemand_state = 1
            purchase_demand.save()

            return redirect('/work/purchase/purchase_demand/')


    return render(request,'purchase/purchase_demand/homepage.html', context=context)
import django
from django.db import reset_queries
from django.shortcuts import redirect, render, reverse
from django.shortcuts import HttpResponseRedirect,HttpResponse
from sympy import det, re
from django.contrib import messages
from purchase import models

# Create your views here.
# 采购部主页
def purchase_home(request):
    return render(request,'purchase/homepage.html')



# 管理供应商信息
def purchase_manage_suppliers_info(request):
    suppliers_info = models.Supplier.objects.all().order_by('supplier_id').values(
        'supplier_id','supplier_name','supplier_add',
        'supplier_charge_name','supplier_charge_phone'
    )

    context = {'suppliers_info':suppliers_info}

    if request.method=='POST':
        if 'edit' in request.POST:
            pass
        elif 'delete' in request.POST:
            pass
        elif 'add' in request.POST:
            pass

    return render(request,'purchase/manage_supplierinfo/homepage.html',context)

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
            return HttpResponseRedirect(reverse('add_supplier'))           # 重定向还不会写
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
            models.Supplier.update_supplier(supplier_id=supplier_id, supplier_name=supplier_name, supplier_add=supplier_add,
                                         supplier_charge_phone=supplier_charge_phone, supplier_charge_name=supplier_charge_name)

            messages.add_message(request, messages.SUCCESS, '更新成功！')
            return redirect('')  # 重定向还不会写
        except ValueError as ve:
            messages.add_message(request, messages.ERROR, ve)
            return redirect('')
    else:
        return render(request, 'purchase/manage_supplierinfo/update.html')



# 制定采购决策
def purchase_make_purchases(request):
    return render(request,'purchase/make_purchase/homepage.html')

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
            old_purchase_order = models.Purchase.objects.get(purchase_id = purchase_id)



            old_purchase_order.save()
            messages.add_message(request, messages.SUCCESS, '更新成功！')

            return redirect('')  # 重定向还不会写
        except models.Supplier.DoesNotExit:
            messages.add_message(request, messages.ERROR, '更新失败，不存在该供应商信息！')
            return redirect('')

    else:
        return render(request,'purchase/make_purchase/update.html')



# 采购需求管理
# 查看采购需求
def purchase_purchase_demands(request):
    return render(request,'purchase/purchase_demand/homepage.html')




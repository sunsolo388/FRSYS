from django.shortcuts import render

# Create your views here.
# 采购部主页
def purchase_home(request):
    return render(request,'purchase/homepage.html')

# 管理供应商信息
def purchase_manage_supplierinfo(request):
    return render(request,'purchase/manage_supplierinfo/homepage.html')
## 添加供应商信息
def purchase_manage_supplierinfo_add(request):
    return render(request,'purchase/manage_supplierinfo/add.html')
## 更新供应商信息
def purchase_manage_supplierinfo_update(request):
    return render(request,'purchase/manage_supplierinfo/update.html')

# 制定采购决策
def purchase_make_purchase(request):
    return render(request,'purchase/make_purchase/homepage.html')
## 添加采购订单
def purchase_make_purchase_add(request):
    return render(request,'purchase/make_purchase/add.html')
## 更新供应商信息
def purchase_make_purchase_update(request):
    return render(request,'purchase/make_purchase/update.html')

# 采购需求管理
# 查看采购需求
def purchase_purchase_demand(request):
    return render(request,'purchase/purchase_demand/homepage.html')
## 更新采购需求
def purchase_purchase_demand_update(request):
    return render(request,'purchase/purchase_demand/update.html')



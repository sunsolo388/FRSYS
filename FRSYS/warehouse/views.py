from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from warehouse import models  # 导入models文件


def warehouse_home(request):
    '''
    仓库主页
    '''
    return render(request,'warehouse/index.html')

def warehouse_inward(request):
    '''
    入库管理
    '''
    return render(request,'warehouse/inward.html')
def warehouse_outward(request):
    '''
    出库管理
    '''
    return render(request,'warehouse/outward.html')
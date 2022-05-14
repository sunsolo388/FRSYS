from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from aftermarket import models as amm
# Create your views here.
# 后台管理售后


def AMtable(request):
    # 跳转到售后表单界面
    if request.method =='GET':
        try :
            aminfo = amm.AM.objects.all()
        except Exception as e:
            aminfo = NULL


        return render(request, 'aftermarket/AMtable.html', locals())
    else:
        am_id=request.POST.get("am_id")
        AMinfo=amm.AM.objects.all()
        return AMdealing(request,am_id)


def AMdealing(request, am_id):
    # 跳转到处理详情界面

    if request.method == 'GET':
        AM_id=am_id
        return render(request, 'aftermarket/AMdealing.html',locals())


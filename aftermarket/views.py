from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
#后台管理售后
def AMlist(request):
    #返回AM的待处理表单界面
    return HttpResponse()

def p1(request):
    #第一个界面，包括售后的相关信息展示
    return HttpResponse()

def p2(request):
    #第二个处理界面，包括处理员的输入相关
    return HttpResponse()

def p3(request):
    #提醒处理完成，与结束按钮
    return HttpResponse()
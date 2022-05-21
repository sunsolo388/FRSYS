from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from login import models  # 导入models文件

# Create your views here.


def register1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        
        if password!=password2:
            messages.add_message(request, messages.ERROR, '两次密码输入不一致，请检查！')
            return render(request, 'homepage/register.html')
        try:
            user_email = models.UserInfo.objects.filter(mail = email)
        except Exception as e:
            user_email = None
        if user_email:
            messages.add_message(request, messages.ERROR, '该用户已存在！请登录！')
            return redirect('/login/')
        else:
        # 将数据保存到数据库
            models.UserInfo.objects.create(
                username=username, pwd=password,
                tel=tel, mail=email, identity=0
            )
            messages.add_message(request, messages.SUCCESS, '注册成功')
            return redirect('/login/')
    elif request.method == 'GET':
        return render(request, 'homepage/register_user.html')

def login1(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = models.UserInfo.objects.get(mail=email)
        except Exception as e:
            user = None
        if user == None:
            messages.add_message(request, messages.ERROR, '不存在该账号，请注册！')
            return redirect('/login/register/')
        if password == user.pwd and user.identity==0:
            messages.add_message(request, messages.SUCCESS, '登录成功')
            return redirect('/userpage/')
        elif password != user.pwd:
            messages.add_message(request, messages.ERROR, '密码错误，登陆失败！')
            return redirect('/login/')
        elif user.identity!=0:
            messages.add_message(request, messages.ERROR, '员工请通过员工通道登录！')
            return redirect('/innerlogin/')

    elif request.method == 'GET':
        return render(request,'homepage/login_user.html')

def register_worker(request):
    if request.method == 'POST':
        dic=dict(
            [(k,v) for v,k in (
                (1, '采购部'), (2, '物流部'), (3, '仓库部'),
                (4, '销售部'), (5, '售后部')
            )]
        )
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        identity = request.POST.get('identity')
        a=dic[identity]
        if password!=password2:
            messages.add_message(request, messages.ERROR, '两次密码输入不一致，请检查！')
            return render(request, 'homepage/register.html')
        try:
            user_email = models.UserInfo.objects.filter(mail = email)
        except Exception as e:
            user_email = None
        if user_email:
            messages.add_message(request, messages.ERROR, '该用户已存在！请登录！')
            return redirect('/innerlogin/')
        else:
        # 将数据保存到数据库
            models.UserInfo.objects.create(
                username=username, pwd=password,
                tel=tel, mail=email, identity=a
            )
            messages.add_message(request, messages.SUCCESS, '注册成功')
            return redirect('/innerlogin/')
    elif request.method == 'GET':
        return render(request, 'homepage/register_worker.html')

def login_worker(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = models.UserInfo.objects.get(mail=email)
        except Exception as e:
            user = None
        if user == None:
            messages.add_message(request, messages.ERROR, '不存在该账号，请注册！')
            return redirect('/innerlogin/innerregister/')
        
        if password == user.pwd:
            messages.add_message(request, messages.SUCCESS, '登录成功')
            if user.identity == 1:
                return redirect('/work/purchase/')
            elif user.identity == 2:
                return redirect('/work/delivery/')
            elif user.identity == 3:
                return redirect('/work/warehouse/')
            elif user.identity == 4:
                return redirect('/work/sales/')
            elif user.identity == 5:
                return redirect('/work/aftermarket/')
        else:
            messages.add_message(request, messages.ERROR, '密码错误，登陆失败！')
            return render(request,'homepage/login_worker.html')
    elif request.method == 'GET':
        return render(request,'homepage/login_worker.html')



def index1(request):
    return render(request,'homepage/index.html')

def about(request):
    return render(request,'homepage/about.html')

def contact(request):
    return render(request,'homepage/contact.html')

def services(request):
    return render(request,'homepage/services.html')

def work(request):
    return render(request, 'homepage/work.html')

def userpage(request):
    return render(request,'df_goods/base.html')
    
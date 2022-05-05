from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from login import models  # 导入models文件

# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        identity = request.POST.get('identity')
        a=0 if identity=='客户' else 1
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
                tel=tel, mail=email, identity=a
            )
            messages.add_message(request, messages.SUCCESS, '注册成功')
            return redirect('/login/')
    elif request.method == 'GET':
        return render(request, 'homepage/register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = models.UserInfo.objects.get(mail=email)
        if password == user.pwd:
            messages.add_message(request, messages.SUCCESS, '登录成功')
            print(user.identity)
            if user.identity == 1:
                return redirect('/work')
            else:
                return render(request,'''<h1>还没做好</h1>''')
        else:
            messages.add_message(request, messages.ERROR, '密码错误，登陆失败！')
    elif request.method == 'GET':
        return render(request,'homepage/login.html')


def index(request):
    return render(request,'homepage/index.html')

def about(request):
    return render(request,'homepage/about.html')

def contact(request):
    return render(request,'homepage/contact.html')

def services(request):
    return render(request,'homepage/services.html')

def work(request):
    return render(request, 'homepage/work.html')
    
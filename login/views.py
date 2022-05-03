from django.shortcuts import render
from login import models  # 导入models文件

# Create your views here.


def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 将数据保存到数据库
        models.UserInfo.objects.create(user=username, pwd=password)

    # 从数据库中读取所有数据，注意缩进
    user_list = models.UserInfo.objects.all()
    return render(request, 'index.html', {'data': user_list})

def login(request):
    return render(request,'homepage/login.html')

def index(request):
    return render(request,'homepage/index.html')

def about(request):
    return render(request,'homepage/about.html')

def contact(request):
    return render(request,'homepage/contact.html')

def services(request):
    return render(request,'homepage/services.html')
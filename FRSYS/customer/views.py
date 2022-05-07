from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from customer import models  # 导入models文件

# Create your views here.
def userpage(request):
    return render(request,'userpage/base.html')
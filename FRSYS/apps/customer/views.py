from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from customer import models  # 导入models文件

import os
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from df_user import user_decorator


@user_decorator.worker
def userpage(request):
    return render(request,'userpage/base.html')
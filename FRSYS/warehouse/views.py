from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import HttpResponse
def index(request):
    return HttpResponse('hello,智者不入爱河！')
 #   return render(request,'index.html')

from django.urls import path

from . import views

urlpatterns = [

    path('/aftermarket/', views.AMtable, name='AMtable'),


    path('/aftermarket/<int:AM_id>/', views.AMdealing, name='AMdealing')
]
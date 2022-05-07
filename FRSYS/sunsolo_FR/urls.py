"""sunsolo_FR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.views.generic.base import RedirectView

from login.views import *
from deliver.views import *
<<<<<<< HEAD
from order.views import *
=======
from aftermarket.views import *
from warehouse.views import *
>>>>>>> cd8b9f6a0d3e3e436f7e0b7bbc33e2b049831b3b

urlpatterns = [
    path('admin/', admin.site.urls),

    # homepage_yly
    path('favicon.ico',RedirectView.as_view(url=r'static/favicon.ico')),
    path('index/',index),
    path('login/',login),
    path('login/register/',register),
    path('index/about/',about),
    path('index/services/',services),
    path('index/contact/',contact),
    path('work/',work),
    path('userpage/',userpage),
    
    # delivery_yly
    path('work/delivery/',deliver_home),
<<<<<<< HEAD
    
    # order_heyueyu
    path('work/sales/',sales_home)
=======
    path('work/delivery/glc/',deliver_glc),
    path('work/delivery/psc/',deliver_psc),


    # aftermarket_dyq
    path('aftermarket/',AMtable),
    path('aftermarket/<int:am_id>/',AMdealing)
>>>>>>> cd8b9f6a0d3e3e436f7e0b7bbc33e2b049831b3b
    
    #warehouse_wxt
    path('work/warehouse/',warehouse_home),
    path('work/warehouse/inward',warehouse_inward),
    path('work/warehouse/outward',warehouse_outward),
]

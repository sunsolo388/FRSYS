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
from django.urls import path, include
from django.urls import re_path as url
from django.views.static import serve  # 上传文件处理函数

from django.views.generic.base import RedirectView

from login.views import *
from deliver.views import *
from purchase.views import *
from order.views import *
from aftermarket.views import *
from warehouse.views import *
from df_cart.views import *
from df_goods.views import *
from df_order.views import *
from df_user.views import *
from .settings import MEDIA_ROOT

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),

    # homepage_yly
    path('favicon.ico', RedirectView.as_view(url=r'static/favicon.ico')),
    path('index/', index1),
    path('login/', login1),
    path('login/register/', register1),
    path('innerlogin/', login_worker),
    path('innerlogin/innerregister/', register_worker),
    path('index/about/', about),
    path('index/services/', services),
    path('index/contact/', contact),
    path('work/', work),

    # userpage
    url(r'^', include('df_goods.urls', namespace='df_goods')),
    url(r'^user/', include('df_user.urls', namespace='df_user')),
    url(r'^cart/', include('df_cart.urls', namespace='df_cart')),
    url(r'^order/', include('df_order.urls', namespace='df_order')),
    url(r'^tinymce/', include('tinymce.urls')),  # 使用富文本编辑框配置confurl
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    # delivery_yly
    path('work/delivery/', deliver_home),
    path('work/delivery/glc/sfyz/', deliver_glc_sfyz),
    path('work/delivery/glc/xqgl/', deliver_glc_xqgl),
    path('work/delivery/glc/rwfp/', deliver_glc_rwfp),
    path('work/delivery/glc/jxz/', deliver_glc_jxz),
    path('work/delivery/glc/ywc/', deliver_glc_ywc),

    path('work/delivery/psc/sfyz/', deliver_psc_sfyz),
    path('work/delivery/psc/<str:staff_id>/dqrw/', deliver_psc_dqrw),
    path('work/delivery/psc/<str:staff_id>/xxsc/', deliver_psc_xxsc),
    path('work/delivery/psc/<str:staff_id>/ywc/', deliver_psc_ywc),

    # order_heyueyu

    path('work/sales/',sales_home),
    path('work/sales/customer_rela/',customer_manage),
    path('work/purchase/order_stats/',order_stats),
    path('work/sales/order_check/a',sales_order_new),  # 待处理订单
    path('work/sales/order_check/c',sales_order_all),  # 全部订单
    path('work/sales/order_check/b',sales_order_correct),  # 订单修改


    # aftermarket_dyq
    path('work/aftermarket/', AMtable),
    path('work/aftermarket/<am_id>/', AMdealing),

    # warehouse_wxt
    path('work/warehouse/', warehouse_home),
    path('work/warehouse/inward', warehouse_inward),
    path('work/warehouse/outward', warehouse_outward),

    # purchase_lxt
    path('work/purchase/', purchase_home),
    path('work/purchase/make_purchase/',purchase_make_purchases),
    path('work/purchase/make_purchase/add/',purchase_make_purchase_add_purchase,name='add_purchase'),
    path('work/purchase/make_purchase/update/',purchase_make_purchase_update_purchase,name='update_purchase'),


    path('work/purchase/manage_supplierinfo/',purchase_manage_suppliers_info),
    path('work/purchase/manage_supplierinfo/add/',purchase_manage_supplierinfo_add_info,name='add_supplier'),
    path('work/purchase/manage_supplierinfo/update/',purchase_manage_supplierinfo_update_info,name='update_supplier'),

    path('work/purchase/purchase_demand/',purchase_purchase_demands,name='purchase_demand_homepage'),
    path('work/purchase/findroot/hp',order_trace,name='find_root'),
    #path('work/purchase/findroot/re',fr_result,name='fr_result'),



]

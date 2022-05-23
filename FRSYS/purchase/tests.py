from django.test import TestCase

# Create your tests here.


''' 溯源功能的实现-后端 '''
from order.models import Order,OrderDetail
from warehouse.models import Inward,WareHouse,Outward
from deliver.models import Deliver,DeliverDetail,CarForDeliver,Car,Staff
from purchase.models import Purchase,PurchaseDetail,Supplier,SupplierDetail
def order_trace(request):
    if request.method == 'POST':
        if 'search_order_trace' in request.POST:
            order_id = request.POST.get('order_id') # 这里看前端到底把这个名字设成啥了

            if order_id:    # 保证有输入内容
                try:
                    # Order实例
                    order = Order.objects.get(order_id = order_id)  # order_time?
                    '''  订单运输过程溯源  '''
                    # Deliver实例
                    deliver_order = order.deliver_id    #
                    car_for_deliver_order = CarForDeliver.objects.get(deliver_id_id = deliver_order.deliver_id)
                    car_order = car_for_deliver_order.car_id  # car_id、cold_chain
                    driver_order = car_order.staff_id   # staff_name
                    # DeliverDetail查询集  这里还需要考虑一个问题，如果这个订单还没发货，从而导致没有DeliverDetail呢
                    deliver_details_order = DeliverDetail.objects.filter(deliver_id_id = deliver_order.deliver_id)  # province、city、detail_time

                    '''  采购过程溯源  '''
                    # OrderDetail查询集
                    order_details = OrderDetail.objects.filter(order_id = order_id)
                    '''  这里的业务逻辑需要沟通  前端需要啥数据 理论上，后端到这儿可以结束了'''
                    for order_detail in order_details:
                        # Outward实例
                        outward = order_detail.outward_id   # out_time
                        # Inward实例
                        inward = outward.warehouse_flow     # in_time
                        ''' 如果还需要Warehouse实例的话，可以用下面这个 不过这个就没办法在前端做到了。后端好像也没法搞'''
                        # 这里获得的是一个WareHouse的查询集，所以我不推荐展示里面的数据
                        # warehouse = WareHouse.objects.filter(warehouse_flow = inward.warehouse_flow)
                        # Purchase实例
                        purchase = inward.purchase_id
                        # PurchaseDetail实例  这里没法在前端完成，所以，还需要进行讨论，该怎么完成
                        purchase_detail = PurchaseDetail.objects.get(purchase_id_id=purchase.purchase_id)   # product_root
                        supplier = purchase_detail.supplier_id  # supplier_name、supplier_add
                        ''' 采购运输过程的溯源 '''
                        # Deliver实例
                        deliver_purchase = purchase.deliver_id
                        car_for_deliver_purchase = CarForDeliver.objects.get(deliver_id_id=deliver_purchase.deliver_id)
                        car_purchase = car_for_deliver_purchase.car_id  # car_id、cold_chain
                        driver_purchase = car_purchase.staff_id  # staff_name
                        # DeliverDetail查询集 这里没法在前端完成，所以，还需要进行讨论，该怎么完成
                        deliver_details_purchase = DeliverDetail.objects.filter(deliver_id_id = deliver_purchase.deliver_id)    # province、city、detail_time


                    '''  溯源过程到此结束  '''

                except Order.DoesNotExist:
                    messages.add_message(request, messages.ERROR, '查询失败！不存在该订单编号！')

    return # 搞不清现在啥情况,返回哪个页面也不明白。前端来搞
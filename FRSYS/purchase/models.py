from django.db import models
from deliver.models import Deliver
from product.models import Product
import time,datetime

# Create your models here.

class Purchase(models.Model):
    '''
    purchase 表
    '''
    purchase_id = models.CharField(max_length=10, primary_key=True, blank=True, verbose_name='采购编号')
    deliver_id = models.ForeignKey(Deliver, on_delete=models.SET_NULL, related_name="purchase_of_this_deliver", null=True)
    purchase_num = models.FloatField(verbose_name='采购数量')
    purchase_time = models.DateTimeField(verbose_name='采购时间')
    purchase_price = models.FloatField(max_length=8, verbose_name='采购的价格')

    # 添加新的采购订单
    @classmethod
    def add_purchase_order(cls,purchase_num, purchase_time, purchase_price, supplier_name, product_name, product_type, product_root):
        # 由supplier_name找到对应的supplier_id
        try:
            supplier = Supplier.objects.get(supplier_name=supplier_name)
        except Supplier.DoesNotExist:
            raise ValueError('没有找到对应的供应商！请更新供应商信息库！')

        # 由product_name找到对应的product_id
        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist:
            # 如果商品库中没有对应商品，就将新商品存入商品库
            product = Product(product_name=product_name, product_type=product_type)
            product.save()

        id = str(int(time.time()))

        # 在创建采购订单时创建对应的物流需求
        deliver = Deliver(deliver_id='CG'+id, start_add = '本公司距离目标最近的基地', aim_add = supplier.supplier_add,
                          apply_time = datetime.datetime.now() )
        deliver.save()

        # 创建对应的采购订单详情
        purchase_detail = PurchaseDetail.add_purchase_detail(purchase_id=id, product_id=product.product_id,
                                                             supplier_id=supplier.supplier_id, product_root=product_root)
        # 创建采购订单
        purchase_order = cls(purchase_id=id, deliver_id = deliver.deliver_id, purchase_num=purchase_num,
                       purchase_time=purchase_time, purchase_price=purchase_price)
        purchase_order.save()

        return purchase_order

    # 更新采购订单
    @classmethod
    def update_purchase_order(cls,purchase_id, purchase_num, purchase_time, purchase_price, supplier_name, product_name, product_type, product_root):
        try:
            old_purchase_order = Purchase.objects.get(purchase_id=purchase_id)
            # 更新Purchase表
            old_purchase_order.purchase_num = purchase_num
            old_purchase_order.purchase_time = purchase_time
            old_purchase_order.purchase_price = purchase_price
            old_purchase_order.save()

            supplier = Supplier.objects.get(supplier_name=supplier_name)
            product = Product.objects.get(product_name=product_name)

        except Purchase.DoesNotExist:
            raise ValueError('更新失败，不存在该订单信息！')
        except Supplier.DoesNotExist:
            raise ValueError('更新失败，不存在该供应商！')
        except Product.DoesNotExist:
            # 如果商品库中没有对应商品，就将新商品存入商品库
            product = Product(product_name=product_name, product_type=product_type)
            product.save()
        finally:
            # 更新PurchaseDetail表
            PurchaseDetail.update_purchase_detail(purchase_id=purchase_id, product_id=product.product_id,
                                              supplier_id=supplier.supplier_id, product_root=product_root)

            return old_purchase_order


class PurchaseDetail(models.Model):
    '''
    purchase_detail 表
    '''
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='purchase_of_this_product')
    supplier_id = models.ForeignKey('Supplier', on_delete=models.DO_NOTHING, related_name='purchase_of_this_supplier')
    product_root = models.TextField()

    # 添加新的采购订单细节
    @classmethod
    def add_purchase_detail(cls, purchase_id, product_id, supplier_id, product_root):
        try:
            purchase_detail_exit = PurchaseDetail.objects.get(purchase_id=purchase_id, product_id=product_id,
                                  supplier_id=supplier_id, product_root=product_root)

            raise ValueError('已存在相同的采购订单！')
        except PurchaseDetail.DoesNotExist:
            purchase_detail = PurchaseDetail(purchase_id=purchase_id, product_id=product_id,
                                  supplier_id=supplier_id, product_root=product_root)
            purchase_detail.save()

            return purchase_detail


    # 更新采购订单细节
    @classmethod
    def update_purchase_detail(cls, purchase_id, product_id, supplier_id, product_root):
        try:
            old_purchase_detail = PurchaseDetail.objects.get(purchase_id=purchase_id)

            old_purchase_detail.product_id = product_id
            old_purchase_detail.supplier_id = supplier_id
            old_purchase_detail.product_root = product_root
            old_purchase_detail.save()

            return old_purchase_detail
        except PurchaseDetail.DoesNotExist:
            raise ValueError('更新失败，该采购订单不存在！')



class Supplier(models.Model):
    '''
    supplier 表
    '''
    supplier_id = models.CharField(max_length=8, primary_key=True, blank=True, verbose_name='供应商编号')
    supplier_add = models.TextField(verbose_name='供应商地址')
    supplier_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='供应商名字')
    supplier_charge_phone = models.PositiveBigIntegerField(verbose_name='供应商负责人电话')
    supplier_charge_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='供应商负责人名字')

    # 添加供应商信息
    @classmethod
    def add_supplier(cls,supplier_add, supplier_charge_phone, supplier_name, supplier_charge_name):
        # 判断数据库中是否已有该数据
        try:
            supplier_exit = Supplier.objects.get(supplier_add=supplier_add,supplier_charge_phone=supplier_charge_phone,
                                            supplier_name=supplier_name,supplier_charge_name=supplier_charge_name)
        except Supplier.DoesNotExist:
            supplier = Supplier(supplier_id=str(int(time.time()) % 100000000),
                           supplier_add=supplier_add, supplier_charge_phone=supplier_charge_phone,
                           supplier_name=supplier_name, supplier_charge_name=supplier_charge_name)

            supplier.save()

            return supplier
        else:
            raise ValueError('已存在该供应商信息！')

    # 更新供应商信息
    @classmethod
    def update_supplier(cls,supplier_id, supplier_add, supplier_charge_phone, supplier_name, supplier_charge_name):
        try:
            old_supplier = Supplier.objects.get(supplier_id=supplier_id)

            old_supplier.supplier_name = supplier_name
            old_supplier.supplier_add = supplier_add
            old_supplier.supplier_charge_name = supplier_charge_name
            old_supplier.supplier_charge_phone = supplier_charge_phone
            old_supplier.save()

            return old_supplier

        except Supplier.DoesNotExit:
            raise ValueError('更新失败，不存在该供应商信息！')


class SupplierDetail(models.Model):
    '''
    supplier_detail 表
    '''
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='supplier_of_this_product')
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='detail_of_this_supplier')


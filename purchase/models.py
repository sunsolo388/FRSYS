from django.db import models
from deliver.models import Deliver
from product.models import Product

# Create your models here.

class Purchase(models.Model):
    '''
    purchase 表
    '''
    purchase_id = models.CharField(max_length=8, primary_key=True, blank=True, verbose_name='采购编号')
    deliver_id = models.ForeignKey(Deliver, on_delete=models.CASCADE,related_name="purchase_deliver")
    purchase_num = models.FloatField(verbose_name='采购数量')
    purchase_time = models.DateTimeField(verbose_name='采购时间')
    purchase_price = models.FloatField(max_length=8, verbose_name='采购的价格')

class Supplier(models.Model):
    '''
    supplier 表
    '''
    supplier_id = models.CharField(max_length=8, primary_key=True, blank=True, verbose_name='供应商编号')
    supplier_add = models.TextField(verbose_name='供应商地址')
    supplier_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='供应商名字')
    supplier_charge_phone = models.PositiveBigIntegerField(verbose_name='供应商负责人电话')
    supplier_charge_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='供应商负责人名字')

class PurchaseDetail(models.Model):
    '''
    purchase_detail 表
    '''
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_root = models.TextField()


class SupplierDetail(models.Model):
    '''
    supplier_detail 表
    '''
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)

class PurchaseDetail(models.Model):
    '''
    purchase_detail 表
    '''
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_root = models.TextField()
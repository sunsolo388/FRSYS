from django.db import models
# Create your models here.
from deliver import models as dm
from purchase.models import Purchase
#from order.models import Order

class Inward(models.Model):
    purchase_id = models.OneToOneField(to=Purchase,to_field="purchase_id",on_delete=models.CASCADE,primary_key=True)
    warehouse_flow = models.CharField(max_length=8,unique=True,default=00000000)
    in_time = models.DateTimeField()
    in_num = models.FloatField(default=0, max_length=8)
    product_name = models.CharField(default='苹果', max_length=20)


class WareHouse(models.Model):
    warehouse_flow = models.ForeignKey(to=Inward,to_field='warehouse_flow',on_delete=models.CASCADE)
    left_num = models.FloatField(max_length=8)
    warehouse_status = models.CharField(max_length=10,default='库存')  #库存or出库
    product_name = product_name = models.CharField(default='苹果', max_length=20)
    class Meta:
        unique_together = ("warehouse_flow","warehouse_status")

class Outward(models.Model):
    outward_id = models.CharField(max_length=8,primary_key=True)
    orderdetail_id = models.CharField(max_length=20)
    warehouse_flow = models.ForeignKey(to=Inward,to_field="warehouse_flow",on_delete=models.CASCADE)
    out_num = models.FloatField(max_length=8)
    out_time = models.DateTimeField()
    product_name = models.CharField(max_length=20)





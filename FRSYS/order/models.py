from django.db import models
from deliver import models as dm
from warehouse import models as wm
from product import models as pm
# Create your models here.
class enterprise_flow(models.Model):
    flow_id = models.CharField(max_length=20,primary_key=True)
    reason = models.TextField()
    num = models.FloatField(max_length=8)
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)


class Customer(models.Model):
    customer_id = models.IntegerField(max_length=4,primary_key=True)
    customer_name = models.CharField(max_length=8)
    customer_tel = models.CharField(max_length=11)
    customer_cre = models.FloatField(max_length=8)
    customer_add = models.TextField()
    #customer_gender = models.BooleanField("性别")

class Order(models.Model):
    order_id = models.CharField(max_length=8,primary_key=True)
    deliver_id = models.ForeignKey(to=dm.Deliver,to_field="deliver_id",on_delete=models.CASCADE)
    customer_id = models.ForeignKey(to=Customer,to_field="customer_id",on_delete=models.CASCADE)
    #warehouse_flow = models.ForeignKey(to=wm.WareHouse,to_field="warehouse_flow",on_delete=models.CASCADE,default='WF100')
    order_price = models.FloatField(max_length=8)
    order_time = models.DateTimeField()



class AfterSales(models.Model):
    aftersales_id = models.CharField(max_length=8,primary_key=True)
    order_id = models.ForeignKey(to=Order,to_field="order_id",on_delete=models.CASCADE)
    question_type = models.CharField(max_length=15)
    question_status = models.BooleanField()
    question_discription = models.TextField()

class OrderDetail(models.Model):
    order_detail_id = models.CharField(max_length=8,primary_key=True)
    order_id = models.ForeignKey(to=Order,to_field="order_id",on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=pm.Product,to_field="product_id",on_delete=models.CASCADE)
    detail_num = models.FloatField(max_length=8)
    outward_id = models.ForeignKey(to=wm.Outward,to_field='outward_id',on_delete=models.CASCADE,null=True,blank=True)
    out_time = models.DateTimeField(null=True,blank=True)


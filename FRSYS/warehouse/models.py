from django.db import models
# Create your models here.
from deliver import models as dm
from purchase.models import Purchase

class Inward(models.Model):
    purchase_id = models.OneToOneField(to=Purchase,to_field="purchase_id",on_delete=models.CASCADE,primary_key=True)
    warehouse_flow = models.CharField(max_length=8,unique=True,default=00000000)
    in_time = models.DateTimeField()
    in_num = models.FloatField(default=0, max_length=8)
    product_name = models.CharField(default='苹果', max_length=20)

class WareHouse(models.Model):
    warehouse_flow = models.OneToOneField(to=Inward,to_field="warehouse_flow",on_delete=models.CASCADE,primary_key=True)
    left_num = models.FloatField(max_length=8)
    warehouse_status = models.CharField(max_length=10)










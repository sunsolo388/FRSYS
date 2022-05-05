from django.db import models
# Create your models here.
from deliver import models as dm
from purchase.models import Purchase

class WareHouse(models.Model):
    warehouse_flow = models.CharField(max_length=8,primary_key=True)
    left_num = models.FloatField(max_length=8)
    warehouse_status = models.CharField(max_length=10)

class Inward(models.Model):
    purchase_id = models.OneToOneField(to=Purchase,to_field="purchase_id",on_delete=models.CASCADE,primary_key=True)
    warehouse_id = models.ForeignKey(to=WareHouse,to_field="warehouse_flow",on_delete=models.CASCADE)
    in_time = models.DateTimeField()


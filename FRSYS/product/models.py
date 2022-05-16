from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=20)
    product_type = models.CharField(max_length=20)
    product_price = models.FloatField(default=0.0, max_length=8)

class PurchaseDemand(models.Model):
    pdemand_id = models.CharField(max_length=8,primary_key=True)
    product_id = models.ForeignKey(to=Product,to_field="product_id",on_delete=models.CASCADE)
    pdemand_num = models.FloatField(max_length=8)
    pdemand_time = models.DateField()
    pdemand_state = models.BooleanField(default=0)


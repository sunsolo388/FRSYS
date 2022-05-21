from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=55)
    product_type = models.CharField(max_length=55)
    product_price = models.FloatField(default=0.0, max_length=8)

class PurchaseDemand(models.Model):
    STATE_UNDONE = 0
    STATE_DONE = 1
    STATE_ITEMS = (
        (STATE_UNDONE, '未完成'),
        (STATE_DONE, '已完成'),
    )

    pdemand_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(to=Product,to_field="product_id",on_delete=models.CASCADE)
    pdemand_num = models.FloatField(max_length=8)
    pdemand_time = models.DateField()
    pdemand_state = models.PositiveIntegerField(default=STATE_UNDONE, choices=STATE_ITEMS, verbose_name="需求状态")



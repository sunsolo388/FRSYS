from django.db import models
from personnel.models import Department,Staff
# Create your models here.

class Deliver(models.Model):
    '''
    deliver 表
    '''
    deliver_id = models.CharField(max_length=8, primary_key=True, verbose_name='物流编号')
    departure_time = models.DateTimeField(verbose_name='离开时间')
    arrival_time = models.DateTimeField(blank=True, null=True, verbose_name='到达时间')

class DeliverDetail(models.Model):
    '''
    deliver_detail 表
    '''
    dd_id = models.CharField(max_length=8, primary_key=True)
    deliver_id = models.ForeignKey(Deliver, on_delete=models.CASCADE)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)


class Car(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    ColdChain_ITEMS = (
        (0, '无冷链车辆'),
        (1, 'A级冷链冷藏车辆'), (2, 'B级冷链冷藏车辆'),
        (3, 'C级冷链冷藏车辆'), (4, 'D级冷链冷藏车辆'),
        (5, 'E级冷链冷藏车辆'), (6, 'F级冷链冷藏车辆'),
        (7, 'G级冷链冷藏车辆'), (8, 'H级冷链冷藏车辆'),
    )

    car_id = models.CharField(max_length=15, verbose_name="车牌号",unique=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    cold_chain = models.PositiveIntegerField(default=0, choices=ColdChain_ITEMS, verbose_name="冷链情况")
    load = models.FloatField(verbose_name="载重")
    staff_id = models.ForeignKey(Staff, verbose_name="司机ID", on_delete=models.DO_NOTHING)

class CarForDeliver(models.Model):
    deliver_id = models.ForeignKey(Deliver,to_field="deliver_id", on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car,to_field="car_id", on_delete=models.CASCADE)
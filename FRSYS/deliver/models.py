from django.db import models
from personnel.models import Department,Staff
from django.utils import timezone
# Create your models here.

class Deliver(models.Model):
    '''
    deliver 表
    '''
    STATUS_ITEMS = (
        (0, '未分配'),
        (1, '已分配'),
        (2, '进行中'),
        (3, '已完成'),
    )
    deliver_id = models.CharField(max_length=8, primary_key=True, verbose_name='物流编号')
    start_add=models.CharField(max_length=30,null=True,verbose_name='出发地点')
    aim_add=models.CharField(max_length=30,null=True, verbose_name='目标地点')
    apply_time=models.DateTimeField(verbose_name='申请时间',default=timezone.now)
    departure_time = models.DateTimeField(null=True,verbose_name='离开时间')
    arrival_time = models.DateTimeField(blank=True, null=True, verbose_name='到达时间')
    status = models.PositiveIntegerField(default=0, choices=STATUS_ITEMS, verbose_name="冷链情况")
    '''
    insert into deliver_deliver (deliver_id,aim_add,start_add,apply_time,status) values('XS000001',"清华","北航",now(),0);
    insert into deliver_deliver (deliver_id,aim_add,start_add,apply_time,status) values('XS000002',"北大","北航",now(),0);
    insert into deliver_deliver (deliver_id,aim_add,start_add,apply_time,status) values('CG000001',"我家","北航",now(),0);
    insert into deliver_deliver (deliver_id,aim_add,start_add,apply_time,status) values('CG000002',"我家","北航",now(),0);
    insert into deliver_deliver (deliver_id,aim_add,start_add,apply_time,status) values('CG000003',"我家","北航",now(),0);
    '''


class DeliverDetail(models.Model):
    '''
    deliver_detail 表
    '''
    dd_id = models.CharField(max_length=8, primary_key=True)
    deliver_id = models.ForeignKey(Deliver, on_delete=models.CASCADE, related_name='detail_of_this_deliver')
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    detail_time = models.DateTimeField(default=timezone.now)
    '''
    insert into deliver_deliverdetail 
    (dd_id,province,city,detail_time,deliver_id_id) 
    values ('DD00001','河北','石家庄',now(),'CG000001');
    insert into deliver_deliverdetail 
    (dd_id,province,city,detail_time,deliver_id_id) 
    values ('DD00002','山西','太原',now(),'CG000001');
    '''


class Car(models.Model):
    STATUS_NORMAL = 0
    STATUS_DELETE = 1
    STATUS_ITEMS = (
        (STATUS_NORMAL, '空闲中'),
        (STATUS_DELETE, '任务中'),
    )
    ColdChain_ITEMS = (
        (0, '无冷链车辆'),
        (1, 'A级冷链冷藏车辆'), (2, 'B级冷链冷藏车辆'),
        (3, 'C级冷链冷藏车辆'), (4, 'D级冷链冷藏车辆'),
        (5, 'E级冷链冷藏车辆'), (6, 'F级冷链冷藏车辆'),
        (7, 'G级冷链冷藏车辆'), (8, 'H级冷链冷藏车辆'),
    )

    car_id = models.CharField(max_length=15,primary_key=True,verbose_name="车牌号",unique=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    cold_chain = models.PositiveIntegerField(default=0, choices=ColdChain_ITEMS, verbose_name="冷链情况")
    load = models.FloatField(verbose_name="载重")
    staff_id = models.ForeignKey(Staff, verbose_name="司机的员工ID", on_delete=models.DO_NOTHING)
    '''
    insert into deliver_car
    values ("京A11111",0,4,20,1);
    insert into deliver_car
    values ("京A11112",0,2,10.5,2);
    insert into deliver_car
    values ("京A11113",0,0,10.5,3);
    insert into deliver_car
    values ("京A11114",0,6,15,5);
    insert into deliver_car
    values ("京A11115",0,1,50.5,6);
    insert into deliver_car
    values ("京A11116",0,3,30.5,7);
    '''

class CarForDeliver(models.Model):
    ''' 这里我想明确一下需求，CarForDeliver与Car、Deliver之间的关系。
    一个Deliver只会对应一个CarForDeliver，一个Car可以对应多个CarForDeliver，我这么理解的对吗？
    那么，我对car_id加一个related_name属性，方便查找Car对应所有CarForDeliver
    '''
    deliver_id = models.ForeignKey(Deliver, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car,to_field="car_id", on_delete=models.DO_NOTHING, related_name='deliver_of_this_car')

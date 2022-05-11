# Generated by Django 4.0.4 on 2022-05-11 09:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True, verbose_name='车牌号')),
                ('status', models.PositiveIntegerField(choices=[(0, '空闲中'), (1, '任务中')], default=0, verbose_name='状态')),
                ('cold_chain', models.PositiveIntegerField(choices=[(0, '无冷链车辆'), (1, 'A级冷链冷藏车辆'), (2, 'B级冷链冷藏车辆'), (3, 'C级冷链冷藏车辆'), (4, 'D级冷链冷藏车辆'), (5, 'E级冷链冷藏车辆'), (6, 'F级冷链冷藏车辆'), (7, 'G级冷链冷藏车辆'), (8, 'H级冷链冷藏车辆')], default=0, verbose_name='冷链情况')),
                ('load', models.FloatField(verbose_name='载重')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='personnel.staff', verbose_name='司机的员工ID')),
            ],
        ),
        migrations.CreateModel(
            name='Deliver',
            fields=[
                ('deliver_id', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='物流编号')),
                ('start_add', models.CharField(max_length=30, null=True, verbose_name='出发地点')),
                ('aim_add', models.CharField(max_length=30, null=True, verbose_name='目标地点')),
                ('apply_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='申请时间')),
                ('departure_time', models.DateTimeField(null=True, verbose_name='离开时间')),
                ('arrival_time', models.DateTimeField(blank=True, null=True, verbose_name='到达时间')),
                ('status', models.PositiveIntegerField(choices=[(0, '未分配'), (1, '已分配'), (2, '进行中'), (3, '已完成')], default=0, verbose_name='冷链情况')),
            ],
        ),
        migrations.CreateModel(
            name='DeliverDetail',
            fields=[
                ('dd_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('detail_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('deliver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_of_this_deliver', to='deliver.deliver')),
            ],
        ),
        migrations.CreateModel(
            name='CarForDeliver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='deliver_of_this_car', to='deliver.car')),
                ('deliver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliver.deliver')),
            ],
        ),
    ]

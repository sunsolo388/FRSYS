# Generated by Django 4.0.4 on 2022-05-03 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deliver',
            fields=[
                ('deliver_id', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='物流编号')),
                ('departure_time', models.DateTimeField(verbose_name='离开时间')),
                ('arrival_time', models.DateTimeField(blank=True, null=True, verbose_name='到达时间')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='部门编号')),
                ('department_name', models.CharField(max_length=50, verbose_name='部门名字')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='员工编号')),
                ('staff_name', models.CharField(max_length=20, verbose_name='员工名字')),
                ('staff_gender', models.CharField(max_length=2, verbose_name='员工性别')),
                ('staff_tel', models.IntegerField(max_length=11, verbose_name='员工电话')),
                ('staff_address', models.CharField(max_length=50, verbose_name='员工家庭地址')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliver.department')),
            ],
        ),
        migrations.CreateModel(
            name='DeliverDetail',
            fields=[
                ('dd_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('deliver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliver.deliver')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.CharField(max_length=15, unique=True, verbose_name='车牌号')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态')),
                ('cold_chain', models.PositiveIntegerField(choices=[(0, '无冷链车辆'), (1, 'A级冷链冷藏车辆'), (2, 'B级冷链冷藏车辆'), (3, 'C级冷链冷藏车辆'), (4, 'D级冷链冷藏车辆'), (5, 'E级冷链冷藏车辆'), (6, 'F级冷链冷藏车辆'), (7, 'G级冷链冷藏车辆'), (8, 'H级冷链冷藏车辆')], default=0, verbose_name='冷链情况')),
                ('load', models.FloatField(verbose_name='载重')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='deliver.staff', verbose_name='司机ID')),
            ],
        ),
    ]

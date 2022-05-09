# Generated by Django 4.0.4 on 2022-05-09 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('staff_tel', models.PositiveBigIntegerField(verbose_name='员工电话')),
                ('staff_address', models.CharField(max_length=50, verbose_name='员工家庭地址')),
                ('department_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_of_this_department', to='personnel.department')),
            ],
        ),
    ]

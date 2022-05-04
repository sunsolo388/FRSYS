from django.db import models

# Create your models here.

class Department(models.Model):
    '''
    department 表
    '''
    department_id = models.CharField(max_length=8, primary_key=True, verbose_name='部门编号')
    department_name = models.CharField(max_length=50, verbose_name='部门名字')

class Staff(models.Model):
    '''
    staff 表
    '''
    staff_id = models.CharField(max_length=8, primary_key=True, verbose_name='员工编号')
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    staff_name = models.CharField(max_length=20, verbose_name='员工名字')
    staff_gender = models.CharField(max_length=2, verbose_name='员工性别')
    staff_tel = models.PositiveBigIntegerField(max_length=11, verbose_name='员工电话')
    staff_address = models.CharField(max_length=50, verbose_name='员工家庭地址')
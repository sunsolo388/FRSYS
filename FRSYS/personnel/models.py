from django.db import models
from django.forms import CharField

# Create your models here.

class Department(models.Model):
    '''
    department 表
    '''
    department_id = models.CharField(max_length=8, primary_key=True, verbose_name='部门编号')
    department_name = models.CharField(max_length=50, verbose_name='部门名字')
    '''
    insert into personnel_department values (5,"售后部");
    insert into personnel_department values (4,"销售部");
    insert into personnel_department values (3,"仓库");
    insert into personnel_department values (2,"物流部");
    insert into personnel_department values (1,"采购部");
    '''

class Staff(models.Model):
    '''
    staff 表
    '''
    staff_id = models.CharField(max_length=8, primary_key=True, verbose_name='员工编号')
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='staff_of_this_department', null=True)
    staff_name = models.CharField(max_length=20, verbose_name='员工名字')
    staff_gender = models.CharField(max_length=2, verbose_name='员工性别')
    staff_tel = models.PositiveBigIntegerField(verbose_name='员工电话')
    staff_address = models.CharField(max_length=50, verbose_name='员工家庭地址')
    position = models.CharField(max_length=10,verbose_name="职务",null=True)
    '''
    insert into personnel_staff
    (staff_id,department_id_id,staff_name,staff_gender,staff_tel,staff_address)
    values(1,2,"配送员1","男",16165,"北航","配送员");
    insert into personnel_staff
    (staff_id,department_id_id,staff_name,staff_gender,staff_tel,staff_address)
    values(2,2,"配送员2","男",10652,"北航","配送员");
    insert into personnel_staff
    (staff_id,department_id_id,staff_name,staff_gender,staff_tel,staff_address)
    values(3,2,"配送员3","女",1064552,"北航","配送员");
    insert into personnel_staff
    (staff_id,department_id_id,staff_name,staff_gender,staff_tel,staff_address)
    values(4,2,"管理员3","女",1064,"北航","管理员");
    '''
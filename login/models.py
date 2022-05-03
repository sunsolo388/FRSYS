from django.db import models

# Create your models here.

class UserInfo(models.Model):
    IDENTITY_CUSTOMER = 0
    IDENTITY_STAFF = 1
    IDENTITY_ITEMS = (
        (IDENTITY_CUSTOMER, '客户'),
        (IDENTITY_STAFF, '员工'),
    )
    username = models.CharField(max_length=20, verbose_name='用户名')
    pwd = models.CharField(max_length=20, verbose_name='密码')
    mail = models.EmailField(verbose_name='邮箱')
    tel_num = models.IntegerField(verbose_name='电话号码')
    identity = models.PositiveIntegerField(default=IDENTITY_CUSTOMER, choices=IDENTITY_ITEMS, verbose_name="状态")

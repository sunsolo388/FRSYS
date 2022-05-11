from django.db import models

# Create your models here.

class UserInfo(models.Model):

    IDENTITY_ITEMS = (
        (0, '客户'),
        (1, '采购部'),
        (2, '物流部'),
        (3, '仓库部'),
        (4, '销售部'),
        (5, '售后部'),
    )
    username = models.CharField(max_length=20, verbose_name='用户名')
    pwd = models.CharField(max_length=20, verbose_name='密码')
    mail = models.EmailField(verbose_name='邮箱')
    tel = models.PositiveBigIntegerField(verbose_name='电话号码')
    identity = models.PositiveIntegerField(default=0, choices=IDENTITY_ITEMS, verbose_name="状态")

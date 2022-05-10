# polls/models.py

import datetime

from django.db import models



class AM(models.Model):
    AM_id=models.CharField(max_length=8,primary_key=True)
    order_id = models.CharField(max_length=8)
    reason_kind=models.CharField(max_length=8)
    reason_detail=models.CharField(max_length=255)
    AM_status=models.CharField(max_length=8)
# insert into aftermarket_am values("am001","o001","退货","奸商卖我烂水果","未处理");
# insert into aftermarket_am values("am002","o002","退货","奸商卖我烂水果","未处理");
# insert into aftermarket_am values("am003","o003","退货","奸商卖我烂水果","未处理");
# insert into aftermarket_am values("am004","o004","退货","奸商卖我烂水果","未处理");
# insert into aftermarket_am values("am005","o005","退货","奸商卖我烂水果","未处理");
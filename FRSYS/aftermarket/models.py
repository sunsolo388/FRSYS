# polls/models.py

import datetime

from django.db import models



class AM(models.Model):
    AM_id=models.CharField(max_length=8)
    order_id=models.CharField(max_length=8)
    reason_kind=models.CharField(max_length=10)
    reason_detail=models.CharField(max_length=50)
    AM_state=models.CharField(max_length=8)



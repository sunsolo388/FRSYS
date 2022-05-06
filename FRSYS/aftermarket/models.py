# polls/models.py

import datetime

from django.db import models
from django.utils import timezone


class AM(models.Model):
    AM_id=models.CharField(max_length=8)
    order_id=models.CharField(max_length=8)
    reason_text=models.CharField(max_length=50)



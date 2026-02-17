import datetime

from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.
class Transaction(models.Model):
    vendor_name = models.CharField(max_length=30)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

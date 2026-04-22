import datetime

from django.db import models
from datetime import date
from django.utils import timezone

CATEGORIES = {
    "OT": "Other", 
	"GR": "Groceries",
	"GS": "Gas",
	"PM": "Payment",
	"SB": "Subscription",
	"EN": "Entertainment",
	"DF": "Dining/Fast Food",
	"UT": "Utilities",
	"FN": "Furniture",
}


# Create your models here.
class Transaction(models.Model):
    vendor_name = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORIES, null=True, blank=True, default=None)

class PDFUpload(models.Model):
    file = models.FileField(upload_to='')
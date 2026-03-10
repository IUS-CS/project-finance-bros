from django.db import models

# Create your models here.
class PdfFile(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdfs/')

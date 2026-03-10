from django import forms
from .models import PdfFile

class PdfForm(forms.ModelForm):
    class Meta:
        model = PdfForm
        fields = ['name', 'file']

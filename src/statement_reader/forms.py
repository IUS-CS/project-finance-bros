from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['vendor_name', 'date', 'amount']

class UploadPDF(forms.Form):
    file = forms.FileField()
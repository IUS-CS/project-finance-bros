from django import forms
from .models import Transaction, CATEGORIES

class TransactionForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORIES, required=True)

    class Meta:
        model = Transaction
        fields = ['vendor_name', 'date', 'amount', 'category']

class UploadPDF(forms.Form): 
    file = forms.FileField()
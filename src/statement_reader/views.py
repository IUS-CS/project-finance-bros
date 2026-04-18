from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory
from django.template import loader
from django.urls import reverse
from .models import Transaction
from .models import PDFUpload
from .forms import TransactionForm
from .forms import UploadPDF
from .handle_uploads import handle_uploaded_file
import os

# Create your views here.
def home(request):
    template = loader.get_template("statement_reader/home.html")
    return HttpResponse(template.render())

def transactions_input(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(transactions_list)
    else:
        form = TransactionForm()
    return render(request, 'statement_reader/transactions_input.html', {'form':form})

def transactions_edit_form(request, pk):
    object = get_object_or_404(Transaction, pk=pk)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect(transactions_list)
    else:
        form = TransactionForm(instance=object)

    return render(request, "statement_reader/transactions_input.html", {'form': form})


def transactions_delete_item(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    transaction.delete()
    return HttpResponseRedirect(reverse('transactions_list'))

def transactions_list(request):
    transactions = Transaction.objects.all()
    template = loader.get_template("statement_reader/transactions_list.html")
    context = {
        'transactions': transactions,
    }
    return HttpResponse(template.render(context, request))

def reader(request):
    template = loader.get_template("statement_reader/reader.html")
    return HttpResponse(template.render({}, request))

@ensure_csrf_cookie
def upload_file(request):
    if request.method == "POST":
        form = UploadPDF(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])  
            specific_transactions = Transaction.objects.filter(category=None)
            TransactionFormSet = modelformset_factory(Transaction, form=TransactionForm, extra=0)
            formset = TransactionFormSet(queryset=specific_transactions)
            return render(request, 'statement_reader/transactions_category_edit.html', {'formset': formset})
                
    else:
        form = UploadPDF()
    return render(request, "statement_reader/reader.html", {"form": form})

def save_categories(request):
    if request.method == 'POST': 
        TransactionFormSet = modelformset_factory(Transaction, fields=('vendor_name', 'date', 'amount', 'category'), extra=0)
        formset = TransactionFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save()
            for instance in instances:
                if instance.category == None:
                    instance.category = 'OT'
                instance.save()
    return redirect(transactions_list)
    
def pdf_list(request):
    pdfs = PDFUpload.objects.all()
    template = loader.get_template("statement_reader/pdf.html")
    context = {
        'pdfs' : pdfs
    }
    return render(request, 'statement_reader/pdf.html', {'pdfs' : pdfs})

def delete_pdf(request, pk):
    pdf = PDFUpload.objects.get(pk=pk)
    pdf.delete()
    return HttpResponseRedirect(reverse('pdf_list'))
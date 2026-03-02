from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Transaction
from .forms import TransactionForm

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

def transactions_list(request):
    transactions = Transaction.objects.all().values()
    template = loader.get_template("statement_reader/transactions_list.html")
    context = {
        'transactions': transactions,
    }
    return HttpResponse(template.render(context, request))

def reader(request):
    template = loader.get_template("statement_reader/reader.html")
    return HttpResponse(template.render())

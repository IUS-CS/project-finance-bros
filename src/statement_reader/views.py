from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def transactions_input(request):
    template = loader.get_template("statement_reader/transactions_input.html")
    return HttpResponse(template.render())

def transactions_list(request):
    template = loader.get_template("statement_reader/transactions_list.html")
    return HttpResponse(template.render())
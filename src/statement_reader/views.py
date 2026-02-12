from django.shortcuts import render

# Create your views here.
def transactions_input(request):
    return render(request,'transactions_input.html')

def transactions_list(request):
    return render(request,'transactions_list.html')
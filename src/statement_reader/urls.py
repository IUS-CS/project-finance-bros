from django.urls import path

from . import views

urlpatterns = [
    path("list", views.transactions_list),
    path("input", views.transactions_input) 
]
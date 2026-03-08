from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("list", views.transactions_list),
    path("input", views.transactions_input),
    path("reader", views.reader),
    path ("edit/<int:pk>/", views.transactions_edit_form, name="transaction_edit_form")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("list", views.transactions_list, name="transactions_list"),
    path("pdf", views.pdf_list, name="pdf_list"),
    path("input", views.transactions_input),
    path("reader", views.reader),
    path("upload", views.upload_file),
    path ("edit/<int:pk>/", views.transactions_edit_form, name="transaction_edit_form"),
    path ("save_categories", views.save_categories, name="transaction_category_edit_form"),
    path ("delete/<int:pk>/", views.transactions_delete_item, name="transaction_delete_item"),
    path ("delete_pdf/<int:pk>/", views.delete_pdf, name="delete_pdf")
]

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Transaction, PDFUpload
from unittest.mock import patch
import datetime

# Create your tests here.
class TransactionInputViewTest(TestCase):
    def test_transaction_page_loads(self):
        response = self.client.get('/input')
        self.assertEqual(response.status_code, 200)

    def test_transaction_post_saves_to_database(self):
        response = self.client.post('/input', {'vendor_name': 'Speedway',
                                              'date': datetime.date.today(),
                                              'amount': '42.00',
					      'category': 'GS'})
        self.assertEqual(Transaction.objects.count(), 1)

class TransactionEditFormTest(TestCase):
    def setUp(self):
        self.transaction = Transaction.objects.create (
            vendor_name = "Speedway",
            amount = 40.00
        )
        self.url = reverse("transaction_edit_form", kwargs={'pk': self.transaction.pk})

    def test_transaction_edit_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_transaction_edit_post_saves_to_database(self):
        response = self.client.post(self.url, data={'vendor_name': 'Thorntons',
                                              'date': datetime.date.today(),
                                              'amount': '42.00',
					      'category': 'GS'})
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.vendor_name, "Thorntons")

class TransactionDeleteItemTest(TestCase):
    def setUp(self):
        Transaction.objects.create(vendor_name = "Walmart", date = datetime.date.today(), amount = 20.00, category = "GR")
        Transaction.objects.create(vendor_name = "Best Buy", date = datetime.date.today(), amount = 60.00, category = "GR")
        self.url = reverse("transaction_delete_item", kwargs={'pk': 1})

    def test_transaction_delete_item_from_database(self):
        response = self.client.get(self.url)
        self.assertEqual(Transaction.objects.count(), 1)

class TransactionInputViewFailTest(TestCase):
    def test_transaction_post_fails_with_too_many_characters_in_vendor(self):
        response = self.client.post('/input', {'vendor_name': 'Speedway1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
                                              'date': datetime.date.today(),
                                              'amount': '42.00',
					      'category': 'GS'})
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_post_fails_with_incorrect_date(self):
        response = self.client.post('/input', {'vendor_name': 'Speedway',
                                              'date': '3/25/asdfg2026',
                                              'amount': '42.00',
					      'category': 'GS'})
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_post_fails_with_incorrect_amount(self):
        response = self.client.post('/input', {'vendor_name': 'Speedway',
                                              'date': datetime.date.today(),
                                              'amount': '$42',
					      'category': 'GS'})
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_post_fails_with_too_many_characters_in_amount(self):
        response = self.client.post('/input', {'vendor_name': 'Speedway',
                                              'date': datetime.date.today(),
                                              'amount': '9999999999999999999999999999999999999999999.00',
					      'category': 'GS'})
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_post_fails_with_no_information(self):
        response = self.client.post('/input')
        self.assertEqual(Transaction.objects.count(), 0)

class TransactionEditFailTest(TestCase):
    def setUp(self):
        self.transaction = Transaction.objects.create (
            vendor_name = "Speedway",
            amount = 40.00
        )
        self.url = reverse("transaction_edit_form", kwargs={'pk': self.transaction.pk})

    def test_transaction_edit_post_fails_with_too_many_characters_in_vendor(self):
        response = self.client.post(self.url, data={'vendor_name': 'Thorntons11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
                                              'date': datetime.date.today(),
                                              'amount': '42.00',
					      'category': 'GS'})
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.vendor_name, "Speedway")

    def test_transaction_edit_post_fails_with_incorrect_date(self):
        response = self.client.post(self.url, data={'vendor_name': 'Thorntons',
                                              'date': '4/2/a2026',
                                              'amount': '42.00',
					      'category': 'GS'})
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.vendor_name, "Speedway")

    def test_transaction_edit_post_fails_with_incorrect_amount(self):
        response = self.client.post(self.url, data={'vendor_name': 'Thorntons',
                                              'date': datetime.date.today(),
                                              'amount': '$42.00',
					      'category': 'GS'})
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.vendor_name, "Speedway")

    def test_transaction_edit_post_fails_with_too_many_characters_in_amount(self):
        response = self.client.post(self.url, data={'vendor_name': 'Thorntons',
                                              'date': datetime.date.today(),
                                              'amount': '9999999999999999999999999999999999999.00',
					      'category': 'GS'})
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.vendor_name, "Speedway")

class PDFUploadInsertTest(TestCase):
    def test_pdfupload_post_saves_to_database(self):
        test_file = SimpleUploadedFile('statement.pdf', b'PDF', content_type='application/pdf')
        with patch("statement_reader.handle_uploads.parse"):
            response = self.client.post('/upload', {'file': test_file})
        self.assertEqual(PDFUpload.objects.count(), 1)

class PDFUploadInsertFailTest(TestCase):
    def test_pdfupload_post_fails_with_no_document(self):
        response = self.client.post('/upload')
        self.assertEqual(PDFUpload.objects.count(), 0)

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Transaction
import datetime

# Create your tests here.
class TransactionInputViewTest(TestCase):
    def test_transaction_page_loads(self):
        response = self.client.get('/input')
        self.assertEqual(response.status_code, 200)

    def test_transaction_post_saves_to_database(self):
        response = self.client.post('/input', {'vendor_name': 'Speedway',
                                              'date': datetime.date.today(),
                                              'amount': '42.00'})
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
                                              'amount': '42.00'})
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.vendor_name, "Thorntons")

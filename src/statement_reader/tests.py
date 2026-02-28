from django.test import TestCase
from django.utils import timezone
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

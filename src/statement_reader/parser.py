from .models import Transaction
from datetime import datetime
import pdfplumber
import re

def parse(file):
    with pdfplumber.open(file.file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

    year = datetime.today().year

    text_regex = re.compile(
        r'^(\d{2}/\d{2})'
        r'(?:\s+\d{2}/\d{2})?'
        r'\s+(.+?)'
        r'\s+\$(\d+\.\d{2})',
        re.MULTILINE,
    )

    for t in text_regex.finditer(text):
        transaction = Transaction(
            date=datetime.strptime(f"{t.group(1)}/{year}", "%m/%d/%Y"),
            vendor_name=t.group(2),
            amount=float(t.group(3)),
        )
        transaction.save()
        
    
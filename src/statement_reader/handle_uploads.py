from .models import PDFUpload
from .parser import parse

def handle_uploaded_file(uploaded_file):
    pdf_upload = PDFUpload(file=uploaded_file)
    pdf_upload.save()
    parse(pdf_upload)
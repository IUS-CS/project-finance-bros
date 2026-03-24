from .models import PDFUpload

def handle_uploaded_file(uploaded_file):
    pdf_upload = PDFUpload(file=uploaded_file)
    pdf_upload.save()
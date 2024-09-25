from django.shortcuts import render, redirect
import boto3
from django.conf import settings
from django.http import JsonResponse
import os
from .models import RESOURCE_METADATA
from django.contrib.auth.models import User
from fpdf import FPDF
from PIL import Image
from io import BytesIO
import tempfile
import pythoncom
from docx import Document
from xlsx2html import xlsx2html
import pdfkit

print("Done checking modules")
# Define extensions
word_extensions = ["doc", "docx"]
excel_extensions = ["xlsx", "xls"]
image_extensions = ["png", "jpg", "bmp", "jpeg", "gif", "tiff", "tif", "webp"]
text_extensions = ["txt"]
pdf_extensions = ["pdf"]

# Page to upload resources
def resourceUploadPage(request):
    return render(request, 'fileUploadTagging.html')

# Function to handle uploading and tagging (keywords) of resource
def resourceUploading(request):
    if 'upload_file' in request.FILES:
        resource = request.FILES['upload_file']
        if resource:
            file_extension = os.path.splitext(resource.name)[1].lower()
            file_type = resource.content_type
            contributor = request.POST.get('contributor')
            resource_name = request.POST.get('resourceName')
            subject = request.POST.get('subject')
            grade = request.POST.get('grade')
            keywords = request.POST.get('keywords')

            print("File extension: ", file_extension)
            print("Contributor: ", contributor)
            print("Resource Name: ", resource_name)
            print("Subject: ", subject)
            print("Grade: ", grade)
            print("Keywords: ", keywords)

            user = User.objects.get(id=contributor)
            RESOURCE_METADATA.objects.create(
                file_type=file_type,
                contributor=user,
                resource_name=resource_name,
                subject=subject,
                grade=grade,
                keywords=keywords
            )
        else:
            return render(request, 'fileUploadTagging.html')
    else:
        print("No file was uploaded - please select a file to upload")

    return redirect("resourceUpload")

def pdfConversionPage(request):
    return render(request, 'pdfConversion.html')

# Function to handle pdf conversion
def resourcePdfConversion(request):
    pythoncom.CoInitialize()
    resource = request.FILES['pdfFile']

    def txt_to_pdf(resource):
        pdf_output = BytesIO()
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        try:
            for line in resource:
                pdf.multi_cell(0, 10, line.decode('utf-8').strip())
        except Exception as e:
            print(f"Error reading the file: {e}")
            return None

        temp_pdf_path = None
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf.output(temp_pdf.name)
            temp_pdf_path = temp_pdf.name
            print(f"Successfully converted to '{temp_pdf.name}'.")

        return temp_pdf_path

    def image_to_pdf(resource):
        pdf_output = BytesIO()
        try:
            image = Image.open(resource)
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            temp_pdf_path = tempfile.mktemp(suffix='.pdf')
            image.save(temp_pdf_path, "PDF", resolution=100.0)
            print(f"Successfully converted to '{temp_pdf_path}'.")

            return temp_pdf_path
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def docx_to_pdf(resource):
        pdf_temp_path = tempfile.mktemp(suffix='.pdf')
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_doc:
                for chunk in resource.chunks():
                    temp_doc.write(chunk)
                temp_doc_path = temp_doc.name

            pypandoc.convert_file(temp_doc_path, 'pdf', outputfile=pdf_temp_path)
            return pdf_temp_path
        except Exception as e:
            print(f"Error during conversion: {e}")
            return None
        finally:
            if 'temp_doc_path' in locals():
                os.remove(temp_doc_path)

    def xlsx_to_pdf(resource):
        pdf_output = BytesIO()
        temp_xlsx_path = None
        temp_pdf_path = None
        temp_html_path = None

        try:
            temp_xlsx_fd, temp_xlsx_path = tempfile.mkstemp(suffix='.xlsx')
            os.close(temp_xlsx_fd)

            with open(temp_xlsx_path, 'wb') as temp_xlsx:
                for chunk in resource.chunks():
                    temp_xlsx.write(chunk)

            # Create a temporary HTML file
            temp_html_fd, temp_html_path = tempfile.mkstemp(suffix='.html')
            os.close(temp_html_fd)

            # Convert XLSX to HTML
            xlsx2html(temp_xlsx_path, temp_html_path)

            # Create a temporary PDF file
            temp_pdf_fd, temp_pdf_path = tempfile.mkstemp(suffix='.pdf')
            os.close(temp_pdf_fd)

            # Convert HTML to PDF
            pdfkit.from_file(temp_html_path, temp_pdf_path)

            with open(temp_pdf_path, "rb") as f:
                pdf_output.write(f.read())

            pdf_output.seek(0)
            return temp_pdf_path

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            for path in [temp_xlsx_path, temp_html_path]:
                if path and os.path.exists(path):
                    os.remove(path)

    def pdf_to_pdfPath(resource):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                for chunk in resource.chunks():
                    temp_pdf.write(chunk)
                temp_pdf_path = temp_pdf.name
            return temp_pdf_path
        except Exception as e:
            print(f"An error occurred while saving the PDF: {e}")
            return None

    if resource:
        extension = os.path.splitext(resource.name)[1][1:]

        if extension in word_extensions:
            print("Converting Word file to PDF")
            pdf_output = docx_to_pdf(resource)
        elif extension in excel_extensions:
            print("Converting Excel file to PDF")
            pdf_output = xlsx_to_pdf(resource)
            print("Temp pdf path: ", pdf_output)
        elif extension in image_extensions:
            print("Converting image file to PDF")
            pdf_output = image_to_pdf(resource)
        elif extension in text_extensions:
            print("Converting text file to PDF")
            pdf_output = txt_to_pdf(resource)
        elif extension in pdf_extensions:
            print("File is already a PDF, saving to temporary path for processing")
            temp_pdf_path = pdf_to_pdfPath(resource)
        else:
            print("Invalid file type; we only support Word, Excel, Image, Text, and PDF files.")
    else:
        print("Invalid file uploaded")

    pythoncom.CoUninitialize()
    return redirect("pdfPage")

# Function to handle watermark/license prepending
def resourceLicencePrepending(request):
    # Code to prepend watermark/license
    resourceFileStorage()  # save the files to the File Storage System
    return None

def uploadPage(request):
    return render(request, 'fileStorage.html')

# Function to handle file system storage
def resourceFileStorage(request):
    if request.method == 'POST' and request.FILES.get('upload_file'):
        file_obj = request.FILES['upload_file']

        s3 = boto3.client(
            's3',
            region_name='af-south-1',  # Replace with your bucket's region
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        try:
            s3.upload_fileobj(
                file_obj,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_obj.name,
                ExtraArgs={'ContentType': file_obj.content_type}
            )
            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_obj.name}"
            return JsonResponse({'file_url': file_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No file uploaded'}, status=400)

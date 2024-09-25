from django.shortcuts import render, redirect
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.views import View
import os
from .models import RESOURCE_METADATA
from django.contrib.auth.models import User
from fpdf import FPDF
from PIL import Image
import win32com.client
from io import BytesIO
import tempfile
import pythoncom
from docx import Document
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import pypandoc
from xlsx2pdf import convert


import pandas as pd
from xlsx2html import xlsx2html
import pdfkit

# Define extensions
word_extensions = ["doc", "docx"]
excel_extensions = ["xlsx", "xls"]
image_extensions = ["png", "jpg", "bmp", "jpeg", "gif", "tiff", "tif", "webp"]
powerpoint_extensions = ["ppt", "pptx"]
text_extensions = ["txt"]
pdf_extensions = ["pdf"]

#page to upload resources
def resourceUploadPage(request):
    return render(request, 'fileUploadTagging.html')

#function to handle uploading and tagging(keywords) of resource
def resourceUploading(request):
    #get all the details of the resource(including file type) alongside the document(s) to upload
    # Check if the file field exists in request.FILES
    if 'upload_file' in request.FILES:
        resource = request.FILES['upload_file']
        if resource:  # Check if a file was actually uploaded
            # Handle the resource upload here
            # e.g., save it or process it
            # Get the file extension
            #CHECK ALL THE EXTENSIONS THAT WE HAVE AVAILABLE WITH THE FILE EXTENSION
            file_extension = os.path.splitext(resource.name)[1].lower()

            #what type of file is being stored as the resource
            file_type = resource.content_type #get from uploaded file

            #get the id of the person uploading the resource
            contributor = request.POST.get('contributor')#fk to the user who uploaded the resource

            #details about the specific resource
            resource_name = request.POST.get('resourceName')
            subject = request.POST.get('subject')
            grade = request.POST.get('grade')

            #keywords contains a list of keywords to find the resource with(need an array later on),delimeter will be used
            keywords = request.POST.get('keywords')

            print("File extension: ", file_extension)
            print("Contributor: ", contributor)
            print("Resource Name: ", resource_name)
            print("Subject: ", subject)
            print("Grade: ", grade)
            print("Keywords: ", keywords)

            user = User.objects.get(id=contributor)
            #save the metadata to RESOURCE_METADATA database model table
            uploadResource = RESOURCE_METADATA.objects.create(file_type=file_type,
            contributor=user,
            resource_name=resource_name,
            subject=subject,
            grade=grade,
            keywords=keywords)

        else:
            # No file uploaded
            return render(request, 'fileUploadTagging.html')
    else:
        # The file field does not exist
        print("No file was uploaded - please select a file to upload")

   
    #get the files ready to be converted to pdf
    #resourcePdfConversion() #pass the files to convert
    return redirect("resourceUpload")

def pdfConversionPage(request):
    return render(request, 'pdfConversion.html')

#function to handle pdf conversion
def resourcePdfConversion(request):
    # Initialize COM
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
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf.output(temp_pdf.name)
            pdf_output.seek(0)
            temp_pdf_path = temp_pdf.name
            print(f"Successfully converted to '{temp_pdf.name}'.")
            # Read the PDF back into BytesIO
            with open(temp_pdf.name, "rb") as f:
                pdf_output.write(f.read())

        pdf_output.seek(0)
        return temp_pdf_path

    def image_to_pdf(resource):
        pdf_output = BytesIO()
        try:
            image = Image.open(resource)
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            # Create a temporary PDF file in the temp directory
            temp_dir = tempfile.gettempdir()
            temp_pdf_path = tempfile.mktemp(suffix='.pdf', dir=temp_dir)

            image.save(temp_pdf_path, "PDF", resolution=100.0)
            print(f"Successfully converted to '{temp_pdf_path}'.")

            # Read the PDF back into BytesIO
            with open(temp_pdf_path, "rb") as f:
                pdf_output.write(f.read())

            pdf_output.seek(0)
            return temp_pdf_path
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def docx_to_pdf(resource):
        # Create a temporary PDF file
        pdf_temp_path = tempfile.mktemp(suffix='.pdf')
        
        try:
            # Save the uploaded DOCX file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_doc:
                for chunk in resource.chunks():
                    temp_doc.write(chunk)
                temp_doc_path = temp_doc.name

            # Convert DOCX to PDF using the temporary file path
            # Add extra args to help with formatting if needed
            pypandoc.convert_file(temp_doc_path, 'pdf', outputfile=pdf_temp_path, extra_args=['--pdf-engine=pdflatex'])
            
            # Return the path to the generated PDF
            return pdf_temp_path
        except Exception as e:
            print(f"Error during conversion: {e}")
            return None
        finally:
            # Clean up the temporary DOCX file
            if 'temp_doc_path' in locals():
                os.remove(temp_doc_path)


    def xlsx_to_pdf(resource):
        pdf_output = BytesIO()
        temp_xlsx_path = None
        temp_html_path = None
        temp_pdf_path = None

        try:
            # Create a temporary XLSX file
            temp_xlsx_fd, temp_xlsx_path = tempfile.mkstemp(suffix='.xlsx')
            os.close(temp_xlsx_fd)

            # Write the uploaded Excel content to the temporary XLSX file
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

            # Read the PDF back into BytesIO
            with open(temp_pdf_path, "rb") as f:
                pdf_output.write(f.read())

            pdf_output.seek(0)
            return pdf_output  # Return the BytesIO object

        except Exception as e:
            print(f"An error occurred: {e}")  # More explicit logging
            return None

        finally:
            # Clean up temporary files
            for path in [temp_xlsx_path, temp_html_path, temp_pdf_path]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError as e:
                        print(f"Error deleting temporary file: {e}")
                
    def pdf_to_pdfPath(resource):
        try:
            # Create a temporary file to save the PDF
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
            print("This is the path you will use further: ", pdf_output)

        elif extension in excel_extensions:
            print("Converting Excel file to PDF")
            pdf_output = xlsx_to_pdf(resource)
            print("This is the path you will use further: ", pdf_output)

        elif extension in image_extensions:
            print("Converting image file to PDF")
            pdf_output = image_to_pdf(resource)
            print("This is the path you will use further: ", pdf_output)

        elif extension in powerpoint_extensions:
            print("Converting PowerPoint file to PDF")
            pdf_output = pptx_to_pdf(resource)
            print("This is the path you will use further: ", pdf_output)

        elif extension in text_extensions:
            print("Converting text file to PDF")
            pdf_output = txt_to_pdf(resource)
            print("This is the path you will use further: ", pdf_output)
            
        elif extension in pdf_extensions:
            print("File is already a PDF, saving to temporary path for processing")
            temp_pdf_path = pdf_to_pdfPath(resource)
            if temp_pdf_path:
                with open(temp_pdf_path, "rb") as f:
                    pdf_output = BytesIO(f.read())
                print(f"Successfully saved PDF to '{temp_pdf_path}'.")
            else:
                print("Failed to save PDF to temporary path.")
            
            print("This is the path you will use further: ", temp_pdf_path)

        else:
            print("Invalid file type; we only support Word, Excel, PowerPoint, Text, Image, and PDF files.")
    else:
        print("Invalid file uploaded")

    # Uninitialize COM
    pythoncom.CoUninitialize()
    return redirect("pdfPage")	

#function to handle watermark/licence prepending
def resourceLicencePrepending(request):
    #get the pdf versions of the resources to be uploaded to file storage

    #prepend the license/watermark to the pdf document(s) 

    #get the files ready to be uploaded to the file storage system
    resourceFileStorage() #save the files to the File Storage System
    return None

def uploadPage(request):
    return render(request, 'fileStorage.html')

#function to handle file system storage
def resourceFileStorage(request):
    if request.method == 'POST' and request.FILES.get('upload_file'):
        # Get the uploaded file from the request
        file_obj = request.FILES['upload_file']

        # Initialize the S3 client using boto3
        s3 = boto3.client(
            's3',
            region_name='af-south-1',  # Replace with your bucket's region
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        # Upload the file to S3
        try:
            s3.upload_fileobj(
                file_obj,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_obj.name,
                ExtraArgs={
                    'ContentType': file_obj.content_type  # Set appropriate content type
                }
            )
            # Return the public URL of the uploaded file
            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_obj.name}"
            return JsonResponse({'file_url': file_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No file uploaded'}, status=400)

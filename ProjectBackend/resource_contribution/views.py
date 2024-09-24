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

#function to handle pdf conversion
def resourcePdfConversion(request):
	resource = request.FILES['upload_file']

	def txt_to_pdf(resource):
		pdf_file = f"{resource.name}.pdf"
		pdf = FPDF()
		pdf.set_auto_page_break(auto=True, margin=15)
		pdf.add_page()
		pdf.set_font("Arial", size=12)

		try:
			for line in resource:
				pdf.multi_cell(0, 10, line.decode('utf-8').strip())
		except Exception as e:
			print(f"Error reading the file: {e}")
			return

		pdfOutput = pdf.output(pdf_file)
		print(pdfOutput.name)
		print(f"Successfully created {pdf_file}")

	def image_to_pdf(resource):
		pdf_filename = f"{resource.name}.pdf"
		try:
			image = Image.open(resource)
			if image.mode in ("RGBA", "LA"):
				image = image.convert("RGB")
			image.save(pdf_filename, "PDF", resolution=100.0)
			print(f"Successfully converted image to '{pdf_filename}'.")
		except Exception as e:
			print(f"An error occurred: {e}")

	def docx_to_pdf(resource):
		pdf_filename = f"{resource.name}.pdf"
		word = win32com.client.Dispatch("Word.Application")

		try:
			doc = word.Documents.Open(resource.name)
			doc.SaveAs(pdf_filename, FileFormat=17)
			print(f"Successfully converted to '{pdf_filename}'.")
			doc.Close(False)
			word.Quit()
		except Exception as e:
			print(f"An error occurred: {e}")

	def pptx_to_pdf(resource):
		pdf_filename = f"{resource.name}.pdf"
		powerpoint = win32com.client.Dispatch("PowerPoint.Application")

		try:
			presentation = powerpoint.Presentations.Open(resource.name, WithWindow=False)
			presentation.SaveAs(pdf_filename, FileFormat=32)
			print(f"Successfully converted to '{pdf_filename}'.")
		except Exception as e:
			print(f"An error occurred: {e}")
		finally:
			presentation.Close()
			powerpoint.Quit()

	def xlsx_to_pdf(resource):
		pdf_filename = f"{resource.name}.pdf"
		excel = win32com.client.Dispatch("Excel.Application")

		try:
			workbook = excel.Workbooks.Open(resource.name)
			workbook.ExportAsFixedFormat(0, pdf_filename)
			print(f"Successfully converted to '{pdf_filename}'.")
		except Exception as e:
			print(f"An error occurred: {e}")
		finally:
			workbook.Close(False)
			excel.Quit()

	# Define extensions
	word_extensions = ["doc", "docx"]
	excel_extensions = ["xlsx", "xls"]
	image_extensions = ["png", "jpg", "bmp", "jpeg", "gif", "tiff", "tif", "webp"]
	powerpoint_extensions = ["ppt", "pptx"]
	text_extensions = ["txt"]
	pdf_extensions = ["pdf"]

	if resource:
		extension = os.path.splitext(resource.name)[1][1:]

		if extension in word_extensions:
			print("Converting Word file to PDF")
			docx_to_pdf(resource)
			
		elif extension in excel_extensions:
			print("Converting Excel file to PDF")
			xlsx_to_pdf(resource)
			
		elif extension in image_extensions:
			print("Converting image file to PDF")
			image_to_pdf(resource)
			
		elif extension in powerpoint_extensions:
			print("Converting PowerPoint file to PDF")
			pptx_to_pdf(resource)
			
		elif extension in text_extensions:
			print("Converting text file to PDF")
			txt_to_pdf(resource)
			
		elif extension in pdf_extensions:
			print("File is already a PDF, ready to proceed to watermarking")
			
		else:
			print("Invalid file type; we only support Word, Excel, PowerPoint, Text, Image, and PDF files.")
	else:
		print("Invalid file uploaded")

	#file_resource.close()  # Ensure the file is closed after processing			
    resourceLicencePrepending() #pass the files to prepend licence to
    return None

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

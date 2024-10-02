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
from docx import Document
from xlsx2html import xlsx2html
import pdfkit
import subprocess
import pypandoc
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File

# Define extensions
word_extensions = ["doc", "docx"]
excel_extensions = ["xlsx", "xls"]
image_extensions = ["png", "jpg", "bmp", "jpeg", "gif", "tiff", "tif", "webp"]
text_extensions = ["txt"]
powerpoint_extensions = ["pptx", "ppt"]
pdf_extensions = ["pdf"]

uploadList = []

# Page to upload resources
def resourceUploadPage(request):
    return render(request, 'fileUploadTagging.html')

# Function to handle uploading and tagging (keywords) of resource
def resourceUploading(request):
    resource_list = []

    if 'upload_file' in request.FILES:
        resource = request.FILES['upload_file']
        if resource != "":
            resource_list.append(resource)

    if 'upload_file1' in request.FILES:
        resource1 = request.FILES['upload_file1']
        if resource1 != "":
            resource_list.append(resource1)

    if 'upload_file2' in request.FILES:
        resource2 = request.FILES['upload_file2']
        if resource2 != "":
            resource_list.append(resource2)

    if 'upload_file3' in request.FILES:
        resource3 = request.FILES['upload_file3']
        if resource3 != "":
            resource_list.append(resource3)


    #for loop to check what file types where uploaded, we only support our 5 file types
    for resource in resource_list:
        #get the values for the resource to be uploaded
        extension = os.path.splitext(resource.name)[1][1:]

        if (extension not in word_extensions) and (extension not in excel_extensions) and (extension not in image_extensions) and (extension not in text_extensions) and (extension not in powerpoint_extensions) and (extension not in pdf_extensions):
            print("Invalid file type for :", resource.name, " - try again(ONLY WORD, EXCEL, POWERPOINT, TEXT, PDF Files)")
            return redirect("resourceUpload")

    #create a list to store the output paths of the licenced pdfs
    licencedPdfList = []

    #for loop to convert my documents into watermarked pdfs
    for resource in resource_list:  
        if resource:
            #get the values for the resource to be uploaded
            file_extension = os.path.splitext(resource.name)[1].lower()
            file_type = resource.content_type

            contributor = request.POST.get('contributor')
            if contributor != "":
                if str(contributor).isdigit():

                    resource_name = request.POST.get('resourceName')
                    if resource_name != "":

                        subject = request.POST.get('subject')
                        if subject != "":

                            grade = request.POST.get('grade')
                            if grade != "":

                                keywords = request.POST.get('keywords')
                                if keywords != "":

                                    
                                    licencedPdfPath = resourcePdfConversion(resource)
                                    if licencedPdfPath is not None:
                                        #add the output for the licenced pdf to the licencedPdfList
                                        licencedPdfList.append(licencedPdfPath)

                                    print("Licenced pdf path: ", licencedPdfPath)

                                else:
                                    print("No keywords provided, provide at least one keyword")
                            else:
                                print("No grade selected, please selecta grade or choose a grade option")
                        else:
                            print("No subject selected, please select a subject or choose an subject option")

                        
                    else:
                        print("Please enter a Resource name")
                else:
                    print("The user id must be an integer")
            else:
                print("There is no contributor, please log in to be a contributor, or enter a contributor user id")
            
        else:
            return render(request, 'fileUploadTagging.html')

    if len(resource_list) == 0:
        print("No file uploaded - upload at least one file to the resource")
        return redirect("resourceUpload")
    else:
        print("This is the licenced pdf list: ", licencedPdfList)

        #call the function to store the files at the paths in the licencedPdfList
        print("LICENECD PATH LIST: ")
        for i in licencedPdfList:
            print(i, "\n")

        print("END OF LICENCED OATH LIST")
        return resourceFileStorage(licencedPdfList, request)

        licencedPdfList = []

        return redirect("resourceUpload")

def pdfConversionPage(request):
    return render(request, 'pdfConversion.html')

# Function to handle pdf conversion
def resourcePdfConversion(resource):
    #resource = request.FILES['pdfFile']

    #function to store the text pdf file to the temp_files folder
    def storeTextPdf(pdf_file_name, pdf):
        file_name = os.path.splitext(pdf_file_name)[0] + '.pdf'
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', file_name)
        # Write file contents
        pdf.output(file_path)

        return file_path

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

        #save the pdf version of the uploaded text file
        file_path = storeTextPdf(resource.name, pdf)

        #prepend licence to the pdf
        watermark_path = resourceLicencePrepending(file_path, resource)

        #delete the original pdf file
        os.remove(file_path)

        return watermark_path

    #function to store the image pdf file to the temp_files folder
    def storeImagePdf(resource, image):
        pdf_file_name = resource.name
        file_name = os.path.splitext(pdf_file_name)[0] + '.pdf'
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', file_name)
        # Write file contents
        image.save(file_path, "PDF", resolution=100.0)

        return file_path

    def image_to_pdf(resource):
        pdf_output = BytesIO()
        try:
            image = Image.open(resource)
            if image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")

            file_path = storeImagePdf(resource, image)

            #prepend licence to the pdf
            watermark_path = resourceLicencePrepending(file_path, resource)

            #delete the original pdf file
            os.remove(file_path)

            return watermark_path
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_miktex():
        script_path = r"scripts\schedule_update.ps1"  # Ensure this path is correct
        command = [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-File", script_path
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("MiKTeX update scheduled successfully.")
        except Exception as e:
            print(f"Error scheduling MiKTeX update: {e}")

    #function to store the doc file to the temp_files folder & as the pdf version
    def storeDoc(resource):
        pdf_file_name = resource.name
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', pdf_file_name)
        
        #store the doc to temp_files
        with open(file_path, 'wb') as file:
            for chunk in resource.chunks():
                file.write(chunk)
        print(f"File saved to: {file_path}")

        #store the pdf based on the stored doc
        return storeDocPdf(file_path, pdf_file_name)

    #function to store the pdf of the docx or doc file
    def storeDocPdf(temp_doc_path, pdf_file_name):
        file_name = os.path.splitext(pdf_file_name)[0] + '.pdf'
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', file_name)
        pypandoc.convert_file(temp_doc_path, 'pdf', outputfile=file_path, extra_args=['--pdf-engine=xelatex'])

        #remove the temporary document file
        #delete the original pdf file
        os.remove(temp_doc_path)

        return file_path

    def docx_to_pdf(resource):
        pdf_temp_path = tempfile.mktemp(suffix='.pdf')
        try:          
            file_path = storeDoc(resource)

            #prepend licence to the pdf
            watermark_path = resourceLicencePrepending(file_path, resource)

            #delete the original pdf file
            os.remove(file_path)

            return watermark_path
        except Exception as e:
            print(f"Error during conversion: {e}")
            return None
        finally:
            if 'temp_doc_path' in locals():
                os.remove(temp_doc_path)

    
    #function to store the excel file to the temp_files folder & as the pdf version
    def storeExcel(resource):
        pdf_file_name = resource.name
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', pdf_file_name)
        
        #store the excel pdf to temp_files
        with open(file_path, 'wb') as file:
            for chunk in resource.chunks():
                file.write(chunk)
        print(f"File saved to: {file_path}")

        #store the html file based on the excel file
        return storeHtmlExcel(file_path, pdf_file_name)

    def storeHtmlExcel(temp_xlsx_path, pdf_file_name):
        file_name = os.path.splitext(pdf_file_name)[0] + '.html'
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', file_name)
        xlsx2html(temp_xlsx_path, file_path)

        #store the pdf version based on the html file
        excel_pdf_file_path = storeExcelPdf(file_path, pdf_file_name)
        
        #delete the excel file
        os.remove(temp_xlsx_path)

        return  excel_pdf_file_path
    
    #function to store the pdf of the docx or doc file
    def storeExcelPdf(temp_html_path, pdf_file_name):
        pdf_output = BytesIO()

        file_name = os.path.splitext(pdf_file_name)[0] + '.pdf'
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', file_name)
        # Convert HTML to PDF
        pdfkit.from_file(temp_html_path, file_path)

        with open(file_path, "rb") as f:
            pdf_output.write(f.read())

        pdf_output.seek(0)

        #delete the html file
        os.remove(temp_html_path)

        return file_path

    def xlsx_to_pdf(resource):
        try:
            #store the excel file along the then pdf version of it
            file_path = storeExcel(resource)
            
            #prepend licence to the pdf
            watermark_path = resourceLicencePrepending(file_path, resource)

            #delete the original pdf
            os.remove(file_path)
            
            return watermark_path

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        #function to store the doc file to the temp_files folder & as the pdf version
    def storePowerpoint(resource):
        pdf_file_name = resource.name
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', pdf_file_name)
        
        #store the powerpoint to temp_files
        with open(file_path, 'wb') as file:
            for chunk in resource.chunks():
                file.write(chunk)

        print(f"File saved to: {file_path}")

        #store the pdf based on the stored doc
        return storePowerpointPdf(file_path, pdf_file_name)

    #function to store the powerpoint as a pdf file in temp_files
    def storePowerpointPdf(temp_pptx_path, pdf_file_name):
        # Set the output PDF path based on the PPTX path
        file_name = os.path.splitext(pdf_file_name)[0] + '.pdf'
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', file_name)

        # Construct the command to convert PPTX to PDF
        command = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(file_path),
            temp_pptx_path
        ]

        # Execute the command and capture output and errors
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #delete the original powerpoint file
        os.remove(temp_pptx_path)

        return file_path

    def pptx_to_pdf(resource):
        temp_pptx_path = None
        temp_pdf_path = None

        try:
            #convert and store the pdf version of the powerpoint
            file_path = storePowerpoint(resource)
        
            #prepend licence to the pdf
            watermark_path = resourceLicencePrepending(file_path, resource)

            #delete the original pdf
            os.remove(file_path)

            return watermark_path

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            # Clean up temporary PPTX file
            if temp_pptx_path and os.path.exists(temp_pptx_path):
                os.remove(temp_pptx_path)
                
    #function to store the excel file to the temp_files folder & as the pdf version
    def storePdf(resource):
        pdf_file_name = resource.name
        file_path = os.path.join(settings.BASE_DIR, 'temp_files', pdf_file_name)
        
        #store the pdf to temp_files
        with open(file_path, 'wb') as file:
            for chunk in resource.chunks():
                file.write(chunk)
        print(f"File saved to: {file_path}")

        return file_path

    def pdf_to_pdfPath(resource):
        try:
            #store the pdf file to the temp_files folder
            file_path = storePdf(resource)

            #prepend licence to the pdf
            watermark_path = resourceLicencePrepending(file_path, resource)

            #remove the original pdf without watermark
            os.remove(file_path)

            return watermark_path
            
        except Exception as e:
            print(f"An error occurred while saving the PDF: {e}")
            return None

    if resource:
        extension = os.path.splitext(resource.name)[1][1:]
        # Call the function to update MiKTeX
        update_miktex()

        if extension in word_extensions:
            print("Converting Word file to PDF")
            pdf_output = docx_to_pdf(resource)
            print("Temp pdf path: ", pdf_output)
            return pdf_output

        elif extension in excel_extensions:
            print("Converting Excel file to PDF")
            pdf_output = xlsx_to_pdf(resource)
            print("Temp pdf path: ", pdf_output)
            return pdf_output

        elif extension in image_extensions:
            print("Converting image file to PDF")
            pdf_output = image_to_pdf(resource)
            print("Temp pdf path: ", pdf_output)
            return pdf_output

        elif extension in text_extensions:
            print("Converting text file to PDF")
            pdf_output = txt_to_pdf(resource)
            print("Temp pdf path: ", pdf_output)
            return pdf_output

        elif extension in powerpoint_extensions:
            print("Converting powerpoint file to PDF")
            pdf_output = pptx_to_pdf(resource) 
            print("Temp pdf path: ", pdf_output)
            return pdf_output
            
        elif extension in pdf_extensions:
            print("File is already a PDF, saving to temporary path for processing")
            temp_pdf_path = pdf_to_pdfPath(resource)
            return temp_pdf_path
        else:
            print("Invalid file type; we only support Word, Excel, Image, Text, and PDF files.")
    else:
        print("Invalid file uploaded")

    return redirect("pdfPage")

#display the watermark page
def watermarkPage(request):
    return render(request, 'watermarkPage.html')

# Function to handle watermark/license prepending
def resourceLicencePrepending(original_pdf_path, resource):
    full_file_name = resource.name

    # Code to prepend watermark/license
    def create_license_pdf(license_text, width, height):
        # Create a PDF with the license text
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        
        # Set initial font and size
        font_name = "Helvetica"
        font_size = 100
        
        # Calculate available text width
        available_width = width - 20  # Leave 10pt margins on each side
        
        # Calculate text width
        text_width = can.stringWidth(license_text, font_name, font_size)
        
        # Shrink font size if text is too wide
        while text_width > available_width and font_size > 6:
            font_size -= 1
            text_width = can.stringWidth(license_text, font_name, font_size)
        
        # Set font and size
        can.setFont(font_name, font_size)

        # Add the license text at coordinates (100, 800)
        can.drawString(10, int(height)/2, license_text)
        can.save()
        
        # Move to the beginning of the BytesIO buffer
        packet.seek(0)
        return packet

    def prepend_license_to_pdf(original_pdf_path, license_text, full_file_name):
        # Read the original PDF
        original_pdf = PdfReader(original_pdf_path)
        
        #get the orientation of the original pdf
        page = original_pdf.pages[0]
        width = page.mediabox.right
        height = page.mediabox.top

        # Create a PDF with the license text
        license_pdf = create_license_pdf(license_text, width, height)
        
        # Create a new PDF writer
        output_pdf = PdfWriter()
        
        # Add the license page first
        license_reader = PdfReader(license_pdf)
        output_pdf.add_page(license_reader.pages[0])
        
        # Add all pages from the original PDF
        for page_num in range(len(original_pdf.pages)):
            output_pdf.add_page(original_pdf.pages[page_num])
        
        file_name = os.path.splitext(resource.name)[0] + '.pdf'
        final_file_name = file_name[::-1] + 'licenced-'[::-1]
        output_pdf_path = os.path.join(settings.BASE_DIR, 'temp_files', final_file_name[::-1])
        
        # Write the combined PDF to a file
        with open(output_pdf_path, 'wb') as output_file:
            output_pdf.write(output_file)


        return output_pdf_path
        #SHOULD THEN DELETE THE ORIGINAL PDF IN THE TEMP_FILES FOLDER

    #license text to add for our watermark
    license_text = "This document is licensed under NexTech License."
    output_path = prepend_license_to_pdf(original_pdf_path, license_text, full_file_name)
    
    #add the output licenced pdf to the uploadList
    uploadList.append(output_path)
    
    #add license to pdf and save the licensed pdf to temp_files
    return output_path

def uploadPage(request):
    return render(request, 'fileStorage.html')



def convert_to_file_like_object(file_path):
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Read the content and create a file-like object
        file_content = f.read()
        # Create an InMemoryUploadedFile object
        file_like_object = InMemoryUploadedFile(
            file=f,
            field_name='upload_file',
            name=os.path.basename(file_path),
            content_type='application/octet-stream',  # Adjust as necessary
            size=os.path.getsize(file_path),
            charset=None
        )

        # Create a BytesIO object from the InMemoryUploadedFile
        file_object = BytesIO(file_like_object.read())
        file_object.seek(0)  # Rewind the file-like object to the beginning

    return file_object, file_like_object

# Function to handle file system storage
def resourceFileStorage(uploadList, request):
    storedList = []
    uploaded_paths_string = ""
    for path in uploadList:
        print("PATH: ", path)
        file_path = path  # Path to your file
        file_obj = convert_to_file_like_object(file_path)[0]
        file_like_object = convert_to_file_like_object(file_path)[1]

        s3 = boto3.client(
            's3',
            region_name='af-south-1', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        try:
            s3.upload_fileobj(
                file_obj,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_like_object.name,
                ExtraArgs={'ContentType': file_like_object.content_type}
            )
            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_like_object.name}"
            print("File uploaded")
            storedList.append(file_url)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    #after storing the file without errors then store the document metadata
    user = request.user
    resource_name = request.POST.get('resourceName')
    subject = request.POST.get('subject')
    grade = request.POST.get('grade')
    keywords = request.POST.get('keywords')

    try:
            
        RESOURCE_METADATA.objects.create(
        #    file_type=file_type,
            contributor=user,
            resource_name=resource_name,
            subject=subject,
            grade=grade,
            keywords=keywords
        )
    except Exception as e:
        print("METADATA ERROR: ",e)
                                

    return JsonResponse({'uploaded_files': storedList}, status=200)
    #return JsonResponse({'error': 'No file uploaded'}, status=400)

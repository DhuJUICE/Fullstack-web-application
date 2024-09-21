from django.shortcuts import render, redirect
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.views import View
import os

# Create your views here.

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
            file_extension = os.path.splitext(resource.name)[1].lower()

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
        else:
            # No file uploaded
            return render(request, 'fileUploadTagging.html')
    else:
        # The file field does not exist
        print("No file was uploaded - please select a file to upload")

    #CHECK ALL THE EXTENSIONS THAT WE HAVE AVAILABLE WITH THE FILE EXTENSION

    #what type of file is being stored as the resource
    #file_type = resource.content_type #get from uploaded file

    #save the metadata to RESOURCE_METADATA database model table

    #get the files ready to be converted to pdf
    #resourcePdfConversion() #pass the files to convert
    return redirect("resourceUpload")

#function to handle pdf conversion
def resourcePdfConversion():
    #get the resource document(s) to convert, must handle a few file types

    #convert the document(s) to pdf

    #get the files ready to be prepended with watermark/licence
    resourceLicencePrepending() #pass the files to prepend licence to
    return None

#function to handle watermark/licence prepending
def resourceLicencePrepending():
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

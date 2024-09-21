from django.shortcuts import render
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.views import View
import os

# Create your views here.
#function to handle uploading and tagging(keywords) of resource
def resourceUploading(request):
	#get all the details of the resource(including file type) alongside the document(s) to upload

	#get the files ready to be converted to pdf
	resourcePdfConversion() #pass the files to convert
	return None

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

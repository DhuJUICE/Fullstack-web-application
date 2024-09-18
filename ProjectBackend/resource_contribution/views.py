from django.shortcuts import render
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.views import View

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
	#get the pdf resource with prepended watermark/license
	print("Working")
	#upload/save the document/resources to the file storage system
	return render(request, 'fileStorage.html')

import os
class UploadFileToS3View(View):
    def post(self, request):
        # Get the uploaded file from the request
        file_obj = request.FILES.get('upload_file')

        if not file_obj:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        # Initialize the S3 client using boto3
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        # Upload the file to S3
        try:
            s3.upload_fileobj(
                file_obj,                           # The file object to upload
                settings.AWS_STORAGE_BUCKET_NAME,    # Your S3 bucket name
                file_obj.name,                      # S3 object name (same as the file name)
                ExtraArgs={
                    'ACL': 'public-read',           # Make file publicly readable (optional)
                    'ContentType': file_obj.content_type  # Set appropriate content type
                }
            )
            # Return the public URL of the uploaded file
            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_obj.name}"
            return JsonResponse({'file_url': file_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

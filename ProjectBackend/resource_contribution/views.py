from django.shortcuts import render

# Create your views here.
#function to handle uploading and tagging(keywords) of resource
def resourceUploading(request):
	#get all the details of the resource(including file type) alongside the document(s) to upload

	#get the files ready to be converted to pdf
	return None

#function to handle pdf conversion
def resourcePdfConversion(request):
	#get the resource document(s) to convert, must handle a few file types

	#convert the document(s) to pdf

	#get the files ready to be prepended with watermark/licence
	return None

#function to handle watermark/licence prepending
def resourceLicencePrepending(request):
	#get the pdf versions of the resources to be uploaded to file storage

	#prepend the license/watermark to the pdf document(s) 

	#get the files ready to be uploaded to the file storage system
	return None

#function to handle file system storage
def resourceFileStorage(request):
	#get the pdf resource with prepended watermark/license

	#upload/save the document/resources to the file storage system
	return None
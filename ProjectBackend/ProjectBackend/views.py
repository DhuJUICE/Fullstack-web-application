from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

def testpage(request):
	return render(request, 'APIdelete.html')

import boto3
from django.http import JsonResponse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def test_s3_connection(request):
    # Initialize a session using your credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIAS66UCUDQ2AC2KBGM',
        #secretAccessHere
        region_name='af-south-1'
    )

    try:
        # Attempt to list the contents of your bucket (even if empty)
        response = s3.list_objects_v2(Bucket='cpmg323-project-file-storage-django')

        # Check if the bucket has contents or not
        if 'Contents' in response:
            return JsonResponse({'status': 'Success', 'message': 'Bucket connected and contains files.'})
        else:
            return JsonResponse({'status': 'Success', 'message': 'Bucket connected but no files found.'})

    except (NoCredentialsError, PartialCredentialsError):
        return JsonResponse({'status': 'Failed', 'message': 'Invalid AWS credentials.'})

    except Exception as e:
        return JsonResponse({'status': 'Failed', 'message': str(e)})



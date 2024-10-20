from django.shortcuts import render, redirect
from .models import RESOURCE_REPORT
from resource_contribution.models import RESOURCE_METADATA
import requests
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def reportPage(request):
    return render(request, 'resourceReport.html')

# Create your views here.
#report certain resource
def resourceReport(request):
    if request.method == 'POST':
        # Get the report complaint and resource ID from the request
        complaint = request.POST.get('reportComplaint')
        resource_id = request.POST.get('resourceId')

        # Validate that complaint is not empty
        if not complaint:
            return JsonResponse({"error": "The complaint field cannot be empty."}, status=400)

        # Validate that resourceId is provided and is a digit
        if not resource_id or not resource_id.isdigit():
            return JsonResponse({"error": "Invalid resource ID. It must be an integer."}, status=400)

        # Check if the resource exists
        try:
            resource = RESOURCE_METADATA.objects.get(id=resource_id)
        except RESOURCE_METADATA.DoesNotExist:
            return JsonResponse({"error": "Resource not found."}, status=404)

        # Assuming the user is authenticated
        user = request.user  # Ensure that the user is logged in

        # Create the report in the database
        report = RESOURCE_REPORT.objects.create(
            reportComplaint=complaint,
            reportResource=resource,
            reportUser=user
        )

        return JsonResponse({"message": "Report created successfully."}, status=201)

    # If the request method is not POST
    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)
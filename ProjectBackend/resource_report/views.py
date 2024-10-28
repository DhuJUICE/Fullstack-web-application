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
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            complaint = data.get('reportComplaint')
            resource_id = data.get('resourceId')

            # Validate that complaint is not empty
            if not complaint:
                return JsonResponse({"error": "The complaint field cannot be empty."}, status=400)

            # Validate that resourceId is provided and is a digit
            if not resource_id or not str(resource_id).isdigit():
                return JsonResponse({"error": "Invalid resource ID. It must be an integer."}, status=400)

            # Check if the resource exists
            try:
                resource = RESOURCE_METADATA.objects.get(id=resource_id)
            except RESOURCE_METADATA.DoesNotExist:
                return JsonResponse({"error": "Resource not found."}, status=404)

            # Ensure that the user is logged in
            if not request.user.is_authenticated:
                return JsonResponse({"error": "User not authenticated."}, status=401)

            # Create the report in the database
            report = RESOURCE_REPORT.objects.create(
                reportComplaint=complaint,
                reportResource=resource,
                reportUser=request.user
            )

            return JsonResponse({"message": "Report created successfully."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    # If the request method is not POST
    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)
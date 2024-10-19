from django.shortcuts import render, redirect
from .models import RESOURCE_REPORT
import requests
import json

def reportPage(request):
    return render(request, 'resourceReport.html')

# Create your views here.
#report certain resource
def resourceReport(request):
    if request.method == 'POST':
        # Get the report complaint from the frontend
        complaint = request.POST.get('reportComplaint')
        resourceId = request.POST.get('resourceId')
        userId = request.user.id  # This line assumes the user is authenticated

        # Validate that complaint is not empty
        if complaint == "":
            print("The complaint field cannot be empty.")
            return redirect("reportPage")

        # Validate that resourceId is a digit (assuming it's an integer ID)
        if resourceId == "":
            print("The resource id field cannot be empty.")
            return redirect("reportPage")
            
        if not resourceId.isdigit():
            print("Invalid input for resourceId, must be an integer.")
            return redirect("reportPage")

        # Prepare data for the API call
        api_url = 'http://127.0.0.1:8000/api/report/deserial'
        
        data = {
            "reportComplaint": complaint,
            "reportResource": resourceId
            # Do not include reportUser here
        }

        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(api_url, json=data, headers=headers)  # Use json=data
            
            if response.status_code == 201:  # 201 for created
                print("Report submitted successfully.")
            else:
                print(f"Failed to submit report. Status code: {response.status_code}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the API request: {e}")

    return redirect("reportPage")
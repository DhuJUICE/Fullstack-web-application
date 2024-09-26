from django.shortcuts import render, redirect
from .models import RESOURCE_REPORT
import requests
import json

def reportPage(request):
    return render(request, 'resourceReport.html')

# Create your views here.
#report certain resource
def resourceReport(request):
    # Get the currently logged-in user - must add resourceUser to the report model
    # user = request.user
    if request.method == 'POST':
        # Get the report complaint from the frontend
        complaint = request.POST.get('reportComplaint')
        resourceId = request.POST.get('resourceId')
        userId = request.POST.get('userId')

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

        # Validate that userId is a digit (assuming it's an integer ID)
        if userId == "":
            print("The user id field cannot be empty.")
            return redirect("reportPage")
        
        if not userId.isdigit():
            print("Invalid input for userId, must be an integer.")
            return redirect("reportPage")

        # If all validations pass, proceed with the API call
        api_url = 'http://127.0.0.1:8000/api/report/deserial'
        
        data = {
            "reportComplaint": complaint,
            "reportResource": resourceId,
            "reportUser": userId
        }

        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(api_url, data=json.dumps(data), headers=headers)
            
            if response.status_code == 200:
                print("Report submitted successfully.")
            else:
                print(f"Failed to submit report. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the API request: {e}")

    return redirect("reportPage")
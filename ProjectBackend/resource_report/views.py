from django.shortcuts import render, redirect
from .models import RESOURCE_REPORT
import requests

# Create your views here.
#resport certain resource
def resourceReport(request):
	"""
	#get the currently logged in user - must add resourceUser to the report model
	user = request.user

	#get the resource compaint from the frontend
	complaint = request.POST.get('resourceComplaint')	
	resource = request.POST.get('resourceId')

	#create the resource report object to be recorded
	report = RESOURCE_REPORT.objects.create(reportResource=resource, reportComplaint=complaint)
	"""

	api_url = 'http://127.0.0.1:8000/api/faq/deserial'  # Replace with your actual API endpoint
	data = {
        'question': 'newQuestion',
        'answer': 'newAnswer'
    }
	headers = {'Content-Type': 'application/json'}
	response = requests.post(api_url, json=data, headers=headers)

	return redirect("api/faq/deserial")

	    
	    
    
    
	#save resource report to database
	return None
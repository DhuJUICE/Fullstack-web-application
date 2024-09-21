from django.shortcuts import render, redirect
from .models import RESOURCE_REPORT
import requests
import json

def reportPage(request):
	return render(request, 'resourceReport.html')

# Create your views here.
#report certain resource
def resourceReport(request):
	#get the currently logged in user - must add resourceUser to the report model
	#user = request.user
	if request.method == 'POST':

		#get the report complaint from the frontend
		complaint = request.POST.get('reportComplaint')	
		resourceId = request.POST.get('resourceId')
		userId = request.POST.get('userId')

		api_url = 'http://127.0.0.1:8000/api/report/deserial'

		data = {
		"reportComplaint": complaint,
		"reportResource": resourceId,
		"reportUser": userId
		}

		headers = {'Content-Type': 'application/json'}
		response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
	return redirect("reportPage")
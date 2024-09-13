from django.shortcuts import render
from .models import RESOURCE_REPORT

# Create your views here.
#resport certain resource
def resourceReport(request):
	#get the currently logged in user - must add resourceUser to the report model
	#user = request.user

	#get the resource compaint from the frontend
	complaint = request.POST.get('resourceComplaint')	
	resource = request.POST.get('resourceId')

	#create the resource report object to be recorded
	report = RESOURCE_REPORT.objects.create(reportResource=resource, reportComplaint=complaint)

	#give/choose resource report complaint


	#save resource report to database
	return None
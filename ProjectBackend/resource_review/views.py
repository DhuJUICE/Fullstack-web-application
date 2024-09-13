from django.shortcuts import render
from resource_contribution.models import RESOURCE_METADATA
# Create your views here.
#get the resources from database and rate them, then save them back in the database
def resourceRating(request):
	#get resources from database with intial empty rating

	#rate the resource

	#save resource with updated rating

	#return the rating page with updated rating
	return None

def moderationPage(request):
	return render(request, 'moderation.html')
    

#get the resources from database and moderate them, then save them back in the database
def resourceModeration(request):

	resource_id = request.POST.get('source_id')
	approval_status = request.POST.get('mod_status')
	moderation_comment = request.POST.get('mod_comment')
	#moderation_date =request.POST.get('mod_dateTime')
	
	#get resource from database with initial empty moderation comment and pending approval
	resource = RESOURCE_METADATA.objects.get(pk=resource_id)
	
	#moderate the resource
	resource.approval_status = approval_status
	resource.moderation_comment = moderation_comment

	#save resource with updated moderation details
	resource.save()

	#return the moderation page with updated moderation details
	return render(request, 'moderation.html')
	
	
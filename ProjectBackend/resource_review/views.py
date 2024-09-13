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

#get the resources from database and moderate them, then save them back in the database
def resourceModeration(request):

	resourceId = '1'
	approval_status = 'approved'
	moderation_comment = 'A cake/cupcake would work rn'
	moderation_date = timezone.now()

	#get resources from database with initial empty moderation comment and pending approval
	resource = RESOURCE_METADATA.objects.get(pk=kwargs['pk'])

	#moderate the resource
	resource.approval_status = approval_status
	resource.moderation_comment = moderation_comment
	moderation_date = timezone.now()

	#save resource with updated moderation details
	resource.save()

	#return the moderation page with updated moderation details
	return None
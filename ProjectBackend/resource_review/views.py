from django.shortcuts import render, redirect, get_object_or_404
from resource_contribution.models import RESOURCE_METADATA

# Create your views here.
def ratingPage(request):
	return render(request, 'rateResource.html')

#get the resources from database and rate them, then save them back in the database
def resourceRating(request):
	resourceId = request.POST.get("resourceId")
	rating = request.POST.get("rating")

	print(resourceId)
	print(rating)

	#get resources from database with intial empty rating
	resource = RESOURCE_METADATA.objects.get(id=resourceId)

	#rate the resource
	resource.resource_rating = rating

	#save resource with updated rating
	resource.save()

	#return the rating page with updated rating
	return render(request, 'rateResource.html')

#get the resources from database and moderate them, then save them back in the database
def resourceModeration(request):
	#get resources from database with intial empty moderation comment and pending approval

	#moderate the resource

	#save resource with updated moderation details

	#return the moderation page with updated moderation details
	return None
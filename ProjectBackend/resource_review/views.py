from django.shortcuts import render, redirect
from resource_contribution.models import RESOURCE_METADATA
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def ratingPage(request):
	return render(request, 'rateResource.html')

#get the resources from database and rate them, then save them back in the database
def resourceRating(request):
    # Check if the request method is POST
    if request.method == "POST":
        resource_id = request.POST.get("resourceId")
        rating = request.POST.get("rating")

        # First, check if the resource exists
        resource = RESOURCE_METADATA.objects.filter(id=resource_id).first()
        if not resource:
            return JsonResponse({"error": "Resource not found."}, status=404)

        # Validate the rating input
        if rating.isdigit() and 1 <= int(rating) <= 5:
            try:
                # Rate the resource
                resource.resource_rating = rating

                # Save resource with updated rating
                resource.save()

                response = {
                    "message": "Resource rated successfully.",
                    "resource_id": resource_id,
                    "rating": rating
                }
                return JsonResponse(response, status=200)

            except Exception as e:
                print(f"An error occurred: {e}")
                return JsonResponse({"error": "An error occurred while saving the rating."}, status=500)

        elif not rating.isdigit():
            return JsonResponse({"error": "Invalid input for rating, must be an integer."}, status=400)
        else:
            return JsonResponse({"error": "Rating must be an integer between 1 and 5."}, status=400)

    # If the request method is not POST
    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

def moderationPage(request):
	return render(request, 'moderation.html')
    

#get the resources from database and moderate them, then save them back in the database
def resourceModeration(request):
    # Check if the request method is POST
    if request.method == "POST":
        resource_id = request.POST.get('source_id')
        approval_status = request.POST.get('mod_status')
        moderation_comment = request.POST.get('mod_comment')
        moderation_date = timezone.now()

        # Validate that resource_id is a digit
        if resource_id.isdigit():
            # Check if resource exists
            try:
                resource = RESOURCE_METADATA.objects.get(pk=resource_id)
            except RESOURCE_METADATA.DoesNotExist:
                return JsonResponse({"error": "Resource not found."}, status=404)

            # Validate approval_status
            if approval_status in ["approved", "rejected"]:
                # Moderate the resource
                resource.approval_status = approval_status
                
                # Check if moderation_comment is not empty
                if moderation_comment:
                    resource.moderation_comment = moderation_comment
                
                # Set the moderation date
                resource.moderation_date = moderation_date

                # Save resource with updated moderation details
                resource.save()

                response = {
                    "message": "Resource moderated successfully.",
                    "resource_id": resource_id,
                    "approval_status": approval_status,
                    "moderation_comment": moderation_comment,
                    "moderation_date": moderation_date.isoformat()
                }
                return JsonResponse(response, status=200)

            else:
                response = {"error": "Invalid input for approval status. Must be 'approved' or 'rejected'."}
                return JsonResponse(response, status=400)
        else:
            response = {"error": "Invalid input for resource_id. Must be an integer."}
            return JsonResponse(response, status=400)

    else:
        response = {"error": "Invalid request method. Only POST is allowed."}
        return JsonResponse(response, status=405)

	
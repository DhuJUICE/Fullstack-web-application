from django.shortcuts import render, redirect
from resource_contribution.models import RESOURCE_METADATA
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

#get the resources from database and rate them, then save them back in the database
from django.http import JsonResponse
from django.db import transaction

@csrf_exempt  # Disable CSRF protection for this view
def resourceRating(request):
    if request.method == "POST":
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)
            resource_id = data.get("resourceId")
            rating = data.get("rating")

            # Check if the resource exists
            resource = RESOURCE_METADATA.objects.filter(id=resource_id).first()
            if not resource:
                return JsonResponse({"error": "Resource not found."}, status=404)

            # Validate the rating input
            if isinstance(rating, int) and 1 <= rating <= 5:
                try:
                    with transaction.atomic():
                        # Rate the resource
                        resource.resource_rating = rating
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

            return JsonResponse({"error": "Rating must be an integer between 1 and 5."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

#get the resources from database and moderate them, then save them back in the database
def resourceModeration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            resource_id = data.get('source_id')
            approval_status = data.get('mod_status')
            moderation_comment = data.get('mod_comment')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

        moderation_date = timezone.now()

        # Validate that resource_id is provided and is a digit
        if resource_id is None:
            return JsonResponse({"error": "Resource ID is required."}, status=400)

        if resource_id.isdigit():
            try:
                resource = RESOURCE_METADATA.objects.get(pk=resource_id)
            except RESOURCE_METADATA.DoesNotExist:
                return JsonResponse({"error": "Resource not found."}, status=404)

            # Validate approval_status
            if approval_status not in ["approved", "rejected"]:
                return JsonResponse({"error": "Invalid input for approval status. Must be 'approved' or 'rejected'."}, status=400)

            # Check if moderation_comment is empty or just whitespace
            if not moderation_comment or not moderation_comment.strip():
                return JsonResponse({"error": "Moderation comment cannot be empty."}, status=400)

            # Moderate the resource
            resource.approval_status = approval_status
            resource.moderation_comment = moderation_comment
            resource.moderation_date = moderation_date
            resource.save()

            response = {
                "message": "Resource moderated successfully.",
                "resource_id": resource_id,
                "approval_status": approval_status,
                "moderation_comment": moderation_comment,
                "moderation_date": moderation_date.isoformat()
            }
            return JsonResponse(response, status=200)

        return JsonResponse({"error": "Invalid input for resource_id. Must be an integer."}, status=400)

    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)
	
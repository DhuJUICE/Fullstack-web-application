from django.shortcuts import render, redirect
from resource_contribution.models import RESOURCE_METADATA
from datetime import datetime

# Create your views here.
def ratingPage(request):
	return render(request, 'rateResource.html')

#get the resources from database and rate them, then save them back in the database
def resourceRating(request):
	try:
		resourceId = request.POST.get("resourceId")
		rating = str(request.POST.get("rating"))

		if rating.isdigit() :
			if int(rating) >= 1 and int(rating) <=5:
				print(resourceId)
				print(rating)

				#get resources from database with intial empty rating
				resource = RESOURCE_METADATA.objects.get(id=resourceId)

				#rate the resource
				resource.resource_rating = rating

				#save resource with updated rating
				resource.save()
			else:
				print("must be integer from 1-5")
		else:
			print("Invalid input for rating, must be integer")

	except Exception as e:
		print(f"An error occurred: {e}")

	#return the rating page with updated rating
	return render(request, 'rateResource.html')

def moderationPage(request):
	return render(request, 'moderation.html')
    

#get the resources from database and moderate them, then save them back in the database
def resourceModeration(request):
    try:
        resource_id = request.POST.get('source_id')
        approval_status = request.POST.get('mod_status')
        moderation_comment = request.POST.get('mod_comment')
        moderation_date = request.POST.get('mod_dateTime')
        
        # Validate that resource_id is a digit
        if resource_id.isdigit():
            # Get resource from database
            resource = RESOURCE_METADATA.objects.get(pk=resource_id)
            
            # Validate approval_status
            if approval_status == "approved" or approval_status == "rejected":
                # Moderate the resource
                resource.approval_status = approval_status
                
                # Check if moderation_comment is not empty
                if moderation_comment != "":
                    resource.moderation_comment = moderation_comment
                    
                    # Validate moderation_date is a valid date
                    try:
                        # Attempt to parse the moderation_date
                        parsed_date = datetime.strptime(moderation_date, '%Y-%m-%d') 
                        resource.moderation_date = parsed_date
                        
                        # Save resource with updated moderation details
                        resource.save()
                    except ValueError:
                        print("Invalid date format for moderation_date. Please use the format YYYY-MM-DD.")
                else:
                    print("You can't leave the comment textfield empty.")
            else:
                print("Invalid input for the approval status, must be \"approved\" or \"rejected\".")
        else:
            print("Invalid input for resource_id, must be an integer.")
    except RESOURCE_METADATA.DoesNotExist:
        print("Resource with the given ID does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Return the moderation page with updated moderation details
    return render(request, 'moderation.html')

	
from django.shortcuts import render
from django.http import JsonResponse
from .models import ANALYTICS

# Create your views here.
def userAnalytics(request):
	method = request.method

	if method == "GET":

		return JsonResponse({'message': 'The user analytics views function is working, this is its response', 'method':method}, status=200)
	elif method == 'POST':
		#create a new analytics record/entry in the database
		event_category = "UserTyping"
		event_action = "Pressed submit"
		event_label = "Moderation"
		user_id = "39"
		event_duration = "2minutes"
		custom_param = "RandomParameter"

		newAnalytics = ANALTICS.objects.create(
			event_category = event_category,
			event_action = event_action,
			event_label = event_label,
			user_id = user_id,
			event_duration = event_duration,
			custom_param = custom_param
		)


		return JsonResponse({
			'event_category' = event_category,
			'event_action' = event_action,
			'event_label' = event_label,
			'user_id' = user_id,
			'event_duration' = event_duration,
			'custom_param' = custom_param,
			status=200
		})
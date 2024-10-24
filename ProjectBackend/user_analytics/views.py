from django.shortcuts import render
from django.http import JsonResponse
from .models import ANALYTICS

def analyticsPage(request):
	return render(request, 'analytics.html')

# Create your views here.
def userAnalytics(request):
	method = request.method

	if method == "GET":
		return JsonResponse({'message': 'The user analytics views function is working, this is its response', 'method':method}, status=200)

	elif method == 'POST':
		#create a new analytics record/entry in the database
		event_category = request.POST.get('event_category')
		event_action = request.POST.get('event_action')
		event_label = request.POST.get('event_label')
		user_id = request.POST.get('user_id')
		event_duration = request.POST.get('event_duration')
		custom_param = request.POST.get('custom_param')

		newAnalytics = ANALYTICS.objects.create(
			event_category = event_category,
			event_action = event_action,
			event_label = event_label,
			user_id = user_id,
			event_duration = event_duration,
			custom_param = custom_param,
		)

		return JsonResponse({
			'event_category':event_category,
			'event_action':event_action,
			'event_label':event_label,
			'user_id':user_id,
			'event_duration':event_duration,
			'custom_param':custom_param},
			status=200
		)

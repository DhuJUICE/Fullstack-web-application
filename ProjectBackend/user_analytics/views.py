from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def userAnalytics(request):
	method = request.method

	if method == "GET":
		return JsonResponse({'message': 'The user analytics views function is working, this is its response', 'method':method}, status=200)
	elif method == 'POST':
		return JsonResponse({'message': 'The user analytics views function is working, this is its response', 'method':method}, status=200)
from django.shortcuts import render
from django.http import JsonResponse
from .models import ANALYTICS
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt  # Use this only for API views; otherwise, handle CSRF properly.
def userAnalytics(request):
    method = request.method
    print("HERE")
    if method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)
            user_id = data.get('userId', 'unknown')
            page = data.get('page', 'unknown')
            event_type = data.get('eventType', 'unknown')
            timestamp = data.get('timestamp')

            # Create a new analytics record
            analytics_record = ANALYTICS.objects.create(
                user_id=user_id,
                page=page,
                event_type=event_type,
                timestamp=timestamp
            )

            return JsonResponse({'message': 'Analytics data saved successfully.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
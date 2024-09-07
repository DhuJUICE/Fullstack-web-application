from django.contrib import admin

from django.urls import path
from .views import deserializeFaqPaginated, deserializeResourcePaginated, deserializeReportPaginated, deserializeUserPaginated
from .views import deserializeFaq, deserializeResource, deserializeReport, deserializeUser
from django.test import TestCase

urlpatterns = [
	#API ENDPOINTS for GET, POST, PUT, DELETE requests

	#deserialized faq endpoint
    path('api/faq/deserial', deserializeFaq.as_view(), name='faq'),
	path('api/faq/deserial/<int:pk>', deserializeFaq.as_view(), name='faq-object'),
	
	#deserialized resource endpoint
	path('api/resource/deserial', deserializeResource.as_view(), name='resource'),
	path('api/resource/deserial/<int:pk>', deserializeResource.as_view(), name='resource-object'),
	
	#deserialized report endpoint
	path('api/report/deserial', deserializeReport.as_view(), name='report'),
	path('api/report/deserial/<int:pk>', deserializeReport.as_view(), name='report-object'),
	
	#deserialized User endpoint
	path('api/user/deserial', deserializeUser.as_view(), name='user'),
	path('api/user/deserial/<int:pk>', deserializeUser.as_view(), name='user-object'),
]

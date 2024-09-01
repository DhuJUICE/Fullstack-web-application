from django.contrib import admin

from django.urls import path
from .views import serializeFaq, serializeResource, serializeReport, serializeUser
from .views import deserializeFaq, deserializeResource, deserializeReport, deserializeUser
from django.test import TestCase


urlpatterns = [
	#serialize routes
	#to see all objects from a table
    path('api/faq/serial/', serializeFaq.as_view(), name='faq-list-create'),
	
	#serialize resource endpoint
	path('api/resource/serial/', serializeResource.as_view(), name='doc-list-create'),
	
	#serialize report endpoint
	path('api/report/serial/', serializeReport.as_view(), name='report-list-create'),
	
	#serialize User endpoint
	path('api/user/serial/', serializeUser.as_view(), name='user-list-create'),


	#deserialize routes
	#deserialize faq endpoint
    path('api/faq/deserial', deserializeFaq.as_view(), name='faq'),
	path('api/faq/deserial/<int:pk>', deserializeFaq.as_view(), name='faq-object'),
	
	#deserialize resource endpoint
	path('api/resource/deserial/', deserializeResource.as_view(), name='resource'),
	path('api/resource/deserial/<int:pk>', deserializeResource.as_view(), name='resource-object'),
	
	#deserialize report endpoint
	path('api/report/deserial/', deserializeReport.as_view(), name='report'),
	path('api/report/deserial/<int:pk>', deserializeReport.as_view(), name='report-object'),
	
	#deserialize User endpoint
	path('api/user/deserial/', deserializeUser.as_view(), name='user'),
	path('api/user/deserial/<int:pk>', deserializeUser.as_view(), name='user-object'),
]

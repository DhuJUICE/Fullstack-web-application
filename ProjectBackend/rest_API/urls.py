from django.contrib import admin

from django.urls import path
from .views import FaqListCreate, DocListCreate, ReportListCreate, UserListCreate, deserializeFaq, deserializeResource, deserializeReport, deserializeUser
from django.test import TestCase


urlpatterns = [
	#serialize routes
	#to see all objects from a table
    path('api/faq/serial/', FaqListCreate.as_view(), name='faq-list-create'),
	
	#serialize resource endpoint
	path('api/resource/serial/', DocListCreate.as_view(), name='doc-list-create'),
	
	#serialize report endpoint
	path('api/report/serial/', ReportListCreate.as_view(), name='report-list-create'),
	
	#serialize User endpoint
	path('api/user/serial/', UserListCreate.as_view(), name='user-list-create'),


	#deserialize routes
	#deserialize faq endpoint
    path('api/faq/deserial', deserializeFaq.as_view(), name='faq'),
	
	#deserialize resource endpoint
	path('api/resource/deserial/', deserializeResource.as_view(), name='doc'),
	
	#deserialize report endpoint
	path('api/report/deserial/', deserializeReport.as_view(), name='report'),
	
	#deserialize User endpoint
	path('api/user/deserial/', deserializeUser.as_view(), name='user'),
]

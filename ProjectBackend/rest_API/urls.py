from django.contrib import admin

from django.urls import path
from .views import deserializeFaqPaginated, deserializeResourcePaginated, deserializeReportPaginated, deserializeUserPaginated
from .views import deserializeFaq, deserializeResource, deserializeReport, deserializeUser
from django.test import TestCase

from .views import ContributorsListView

urlpatterns = [
    
	path('api/contributors', ContributorsListView.as_view(), name='contributors-list'),
	#API ENDPOINTS for GET, POST, PUT, DELETE requests

	#with pagination for GET requests of all objects
	path('api/faq/deserial/paginated', deserializeFaqPaginated.as_view(), name='faq-paginated'),
	path('api/resource/deserial/paginated', deserializeResourcePaginated.as_view(), name='resource-paginated'),
	path('api/report/deserial/paginated', deserializeReportPaginated.as_view(), name='report-paginated'),
	path('api/user/deserial/paginated', deserializeUserPaginated.as_view(), name='user-paginated'),

	#No pagination for GET requests
	#faq endpoints
    path('api/faq/deserial', deserializeFaq.as_view(), name='faq'),
	path('api/faq/deserial/<int:pk>', deserializeFaq.as_view(), name='faq-object'),
	
	#resource endpoints
	path('api/resource/deserial', deserializeResource.as_view(), name='resource'),
	path('api/resource/deserial/<int:pk>', deserializeResource.as_view(), name='resource-object'),
	
	#report endpoints
	path('api/report/deserial', deserializeReport.as_view(), name='report'),
	path('api/report/deserial/<int:pk>', deserializeReport.as_view(), name='report-object'),
	
	#User endpoints
	path('api/user/deserial', deserializeUser.as_view(), name='user'),
	path('api/user/deserial/<int:pk>', deserializeUser.as_view(), name='user-object'),
]

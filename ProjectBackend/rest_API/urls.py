from django.contrib import admin

from django.urls import path
from .views import FaqListCreate, FaqDetail, DocListCreate, ReportListCreate, UserListCreate

urlpatterns = [
	#faq endpoint
	#to see all objects from a table
    path('api/faq/', FaqListCreate.as_view(), name='faq-list-create'),
	
	#to see the detail about a specific object in a table or from tables
    #path('api/faq/<int:pk>/', FaqDetail.as_view(), name='faq-detail'),
	
	#resource endpoint
	path('api/resource/', DocListCreate.as_view(), name='doc-list-create'),
	
	#report endpoint
	path('api/report/', ReportListCreate.as_view(), name='report-list-create'),
	
	#User endpoint
	path('api/user/', UserListCreate.as_view(), name='user-list-create'),
]

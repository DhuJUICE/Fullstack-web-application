from django.contrib import admin

from django.urls import path
from .views import FaqListCreate, FaqDetail, DocListCreate

urlpatterns = [
    path('api/faq/', FaqListCreate.as_view(), name='faq-list-create'),
    path('api/faq/<int:pk>/', FaqDetail.as_view(), name='faq-detail'),
	
	path('api/resource/', DocListCreate.as_view(), name='doc-list-create'),
]

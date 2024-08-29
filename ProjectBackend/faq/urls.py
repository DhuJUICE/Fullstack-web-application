from django.contrib import admin

from django.urls import path
from .views import FaqListCreate, FaqDetail

urlpatterns = [
    path('books/', FaqListCreate.as_view(), name='faq-list-create'),
    #path('books/<int:pk>/', FaqDetail.as_view(), name='faq-detail'),
]

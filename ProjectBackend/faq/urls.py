from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	#url to display all faqs from database
    path('faqs', displayFaqs, name='faqs-display'),
]

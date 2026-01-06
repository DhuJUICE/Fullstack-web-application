from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('resourceReport', views.resourceReport, name='resourceReport'),
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('reportPage', views.reportPage, name='reportPage'),
    path('resourceReport', views.resourceReport, name='resourceReport'),
]

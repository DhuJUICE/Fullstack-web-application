from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('resourceContribution', views.resourceUploading, name='resourceContribution'),
    path('uploadPage', views.uploadPage, name='uploadPage'),
    path('fileStorage', views.resourceFileStorage, name='fileStorage')
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('resourceContribution', views.resourceUploading, name='resourceContribution'),
    path('uploadPage', views.uploadPage, name='uploadPage'),
    path('fileStorage', views.resourceFileStorage, name='fileStorage'),

	path('resourceUpload', views.resourceUploadPage, name='resourceUpload'),
	path('resourceUploadTagging', views.resourceUploading, name='resourceUploadTagging'),

	path('pdfPage', views.pdfConversionPage, name='pdfPage'),
	path('pdfConversion', views.resourcePdfConversion, name='pdfConversion'),
]

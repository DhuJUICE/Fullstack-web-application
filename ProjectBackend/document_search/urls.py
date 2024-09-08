from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('resourceSearch', views.resourceSearch, name='resourceSearch'),
]

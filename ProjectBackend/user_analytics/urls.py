from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('pageName', views.functionName, name='functionName'),
]
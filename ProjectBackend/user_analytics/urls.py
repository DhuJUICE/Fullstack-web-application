from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('analytics-page', views.analyticsPage, name='analytics-page'),
    path('analytics', views.userAnalytics, name='analytics'),
]

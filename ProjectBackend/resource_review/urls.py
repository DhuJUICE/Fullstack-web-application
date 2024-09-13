from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('ratingPage', views.ratingPage, name='ratingPage'),
    path('resourceRating', views.resourceRating, name='resourceRating'),
    path('resourceModeration', views.resourceModeration, name='resourceModeration')
]

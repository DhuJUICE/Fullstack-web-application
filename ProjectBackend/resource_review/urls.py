from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('resourceRating', views.resourceRating, name='resourceRating'),
    path('moderationPage', views.moderationPage, name='moderationPage'),
    path('resourceModeration', views.resourceModeration, name='resourceModeration')
]

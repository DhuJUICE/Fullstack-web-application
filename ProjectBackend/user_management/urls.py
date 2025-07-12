from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	#define the homepage url
	path('getUserRole', views.userRole, name='userRole'),
	path('', views.homepage, name='homepage'),
    path('register', views.registerUser, name='registerButton'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('validateCode', views.validate_verification_code, name='validateCode'),
	path('changePassword', views.changePassword, name='changePassword'),
	path('updateRole', views.updateRole, name='updateRole'),
]
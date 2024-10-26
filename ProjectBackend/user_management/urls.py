from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	#define the homepage url
	path('getUserRole', views.userRole, name='userRole'),

	path('', views.homepage, name='homepage'),

    path('loginpage', views.loginPage, name='loginPage'),
    path('registerpage', views.registerPage, name='registerPage'),

    path('login', views.loginUser, name='login'),
    path('register', views.registerUser, name='registerButton'),
    path('logout', views.logout, name='logout'),

    path('resetPasswordPage', views.resetPasswordPage, name='resetPasswordPage'),
    path('resetPassword', views.resetPassword, name='resetPassword'),

	path('validateCodePage', views.validateCodePage, name='validateCodePage'),
    path('validateCode', views.validate_verification_code, name='validateCode'),

	path('changePasswordPage', views.changePasswordPage, name='changePasswordPage'),
	path('changePassword', views.changePassword, name='changePassword'),

	path('updateRolePage', views.updateRolePage, name='updateRolePage'),
	path('updateRole', views.updateRole, name='updateRole'),
]
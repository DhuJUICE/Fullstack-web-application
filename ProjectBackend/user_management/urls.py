from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('loginpage', views.loginPage, name='loginPage'),
    path('registerpage', views.registerPage, name='registerPage'),

    path('login', views.loginUser, name='login'),
    path('register', views.registerUser, name='registerButton'),
    path('logout', views.logout, name='logout'),

    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('testpage', views.testPage, name='testpage')
]
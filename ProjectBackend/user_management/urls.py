from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('loginpage', views.loginPage, name='loginPage'),
    path('login', views.loginUser, name='login'),
    path('registerpage', views.registerPage, name='registerPage'),
    path('register', views.registerUser, name='registerButton'),
    path('testpage', views.testPage, name='testpage')
]
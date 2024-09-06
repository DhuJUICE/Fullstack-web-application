from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('loginpage', views.loginPage, name='loginPage'),
    path('login', views.loginButton, name='login'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('register', views.registerButton, name='registerButton'),
    path('testpage', views.testPage, name='testpage')
]
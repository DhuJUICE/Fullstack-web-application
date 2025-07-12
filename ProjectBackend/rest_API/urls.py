from django.test import TestCase
from django.contrib import admin
from django.urls import path

from .views import deserializeFaqPaginated, deserializeResourcePaginated, deserializeReportPaginated, deserializeUserPaginated, deserializeAnalyticsPaginated, deserializeProfilePaginated
from .views import deserializeFaq, deserializeResource, deserializeReport, deserializeUser, deserializeAnalytics, deserializeProfile
from .views import ContributorsListView
from .views import Login, Register, Logout, ResetPassword, ValidateCode, NewPassword, UpdateUserRole
from .views import ResourceModeration, ResourceRating, ResourceReport, ResourceContribute, UserAnalytics
from .views import tokenPage, tokenRefreshPage, GetUserRole

#token view imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	#return the users role on login usint the api/token endpoint
	path('api/role', GetUserRole.as_view(), name='user-role'),

    path('api/token', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

	#User Analytics API endpoints
	path('api/analytics', UserAnalytics.as_view(), name='api-analytics'),

	#Contribute Resource API endpoints
	path('api/contribute-resource', ResourceContribute.as_view(), name='api-contribute_resource'),

	#Report Resource API endpoints
	path('api/report-resource', ResourceReport.as_view(), name='api-report_resource'),

	#Resource Review API endpoints
	path('api/moderate-resource', ResourceModeration.as_view(), name='api-moderate_resource'),
	path('api/rate-resource', ResourceRating.as_view(), name='api-rate_resource'),

	#User Management API endpoints
	path('api/update-role', UpdateUserRole.as_view(), name='api-update_user_role'),
	
	path('api/new-password', NewPassword.as_view(), name='api-new_password'),
	path('api/validate-code', ValidateCode.as_view(), name='api-validate_code'),
	path('api/reset-password', ResetPassword.as_view(), name='api-reset_password'),
	path('api/register', Register.as_view(), name='api-register'),

	path('api/contributors', ContributorsListView.as_view(), name='contributors-list'),
	#API ENDPOINTS for GET, POST, PUT, DELETE requests

	#User Profile endpoints
	path('api/user-profile/deserial', deserializeProfile.as_view(), name='user-analytics'),
	path('api/user-profile/deserial/<int:pk>', deserializeProfile.as_view(), name='user-analytics-object'),

	#user analytics endpoints
	path('api/analytics/deserial', deserializeAnalytics.as_view(), name='user-analytics'),
	path('api/analytics/deserial/<int:pk>', deserializeAnalytics.as_view(), name='user-analytics-object'),

	#faq endpoints
    path('api/faq/deserial', deserializeFaq.as_view(), name='faq'),
	path('api/faq/deserial/<int:pk>', deserializeFaq.as_view(), name='faq-object'),
	
	#resource endpoints
	path('api/resource/deserial', deserializeResource.as_view(), name='resource'),
	path('api/resource/deserial/<int:pk>', deserializeResource.as_view(), name='resource-object'),
	
	#report endpoints
	path('api/report/deserial', deserializeReport.as_view(), name='report'),
	path('api/report/deserial/<int:pk>', deserializeReport.as_view(), name='report-object'),
	
	#User endpoints
	path('api/user/deserial', deserializeUser.as_view(), name='user'),
	path('api/user/deserial/<int:pk>', deserializeUser.as_view(), name='user-object'),
]

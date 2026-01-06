from django.test import TestCase
from django.contrib import admin
from django.urls import path

from .views import *

#token view imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

	path('api/role', GetUserRole.as_view(), name='user-role'),
	path('api/analytics', UserAnalytics.as_view(), name='api-analytics'),
	path('api/contribute-resource', ResourceContribute.as_view(), name='api-contribute_resource'),
	path('api/report-resource', ResourceReport.as_view(), name='api-report_resource'),
	path('api/moderate-resource', ResourceModeration.as_view(), name='api-moderate_resource'),
	path('api/rate-resource', ResourceRating.as_view(), name='api-rate_resource'),
	path('api/update-role', UpdateUserRole.as_view(), name='api-update_user_role'),
	path('api/new-password', NewPassword.as_view(), name='api-new_password'),
	path('api/validate-code', ValidateCode.as_view(), name='api-validate_code'),
	path('api/reset-password', ResetPassword.as_view(), name='api-reset_password'),
	path('api/register', Register.as_view(), name='api-register'),
	path('api/contributors', ContributorsListView.as_view(), name='contributors-list'),

	path('api/user-profile', deserializeProfile.as_view(), name='user-analytics'),
	path('api/user-profile/<int:pk>', deserializeProfile.as_view(), name='user-analytics-object'),
	path('api/analytics', deserializeAnalytics.as_view(), name='user-analytics'),
	path('api/analytics/<int:pk>', deserializeAnalytics.as_view(), name='user-analytics-object'),
    path('api/faq', deserializeFaq.as_view(), name='faq'),
	path('api/faq/<int:pk>', deserializeFaq.as_view(), name='faq-object'),
	path('api/resource', deserializeResource.as_view(), name='resource'),
	path('api/resource/<int:pk>', deserializeResource.as_view(), name='resource-object'),
	path('api/report', deserializeReport.as_view(), name='report'),
	path('api/report/<int:pk>', deserializeReport.as_view(), name='report-object'),
	path('api/user', deserializeUser.as_view(), name='user'),
	path('api/user/<int:pk>', deserializeUser.as_view(), name='user-object'),
]

from django.contrib import admin

from django.urls import path
from .views import serializeFaq, serializeResource, serializeReport, serializeUser
from .views import deserializeFaq, deserializeResource, deserializeReport, deserializeUser

urlpatterns = [
    # Serialize routes
    path('api/faq/serial/', serializeFaq.as_view(), name='faq-list-create'),
    path('api/resource/serial/', serializeResource.as_view(), name='doc-list-create'),
    path('api/report/serial/', serializeReport.as_view(), name='report-list-create'),
    path('api/user/serial/', serializeUser.as_view(), name='user-list-create'),

    # Deserialize routes
    path('api/faq/deserial/', deserializeFaq.as_view(), name='faq-create'),
    path('api/faq/deserial/<int:pk>/', deserializeFaq.as_view(), name='faq-detail'),
    path('api/resource/deserial/', deserializeResource.as_view(), name='doc-create'),
    path('api/resource/deserial/<int:pk>/', deserializeResource.as_view(), name='doc-detail'),
    path('api/report/deserial/', deserializeReport.as_view(), name='report-create'),
    path('api/report/deserial/<int:pk>/', deserializeReport.as_view(), name='report-detail'),
    path('api/user/deserial/', deserializeUser.as_view(), name='user-create'),
    path('api/user/deserial/<int:pk>/', deserializeUser.as_view(), name='user-detail'),
]


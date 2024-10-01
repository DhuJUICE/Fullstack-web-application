"""
URL configuration for ProjectBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="NexTech RESTAPI",
        default_version='v1',
        description="This api will serve data from our Share2Teach Backend with any Frontend",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    #this path is for testing out AWS S3 file storage system connection to the backend
    #path('test-s3/', views.test_s3_connection, name='test_s3_connection'),

    #include other APPs url routings
    path('', include('resource_contribution.urls')),
    path('', include('resource_review.urls')),
    path('', include('resource_report.urls')),
    path('', include('user_management.urls')),
    path('', include('document_search.urls')),
    path('', include('user_analytics.urls')),
    path('', include('faq.urls')),
	path('', include('rest_API.urls')),

	#documentation urls
	path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('openapi', schema_view.without_ui(cache_timeout=0), name='schema-openapi'),
]




from django.shortcuts import render
from rest_framework import generics

from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA
from resource_report.models import RESOURCE_REPORT
from django.contrib.auth.models import User, auth

from .serializers import FaqSerializer, DocSerializer, ReportSerializer, UserSerializer
from rest_framework.permissions import AllowAny

#class based views to show the detail of all objects
class FaqListCreate(generics.ListCreateAPIView):
    #f1 = FAQ.objects.create(question="Are you ready?", answer="Yes my guy")
    #f1.save()
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
	#who can get access to the objects, will be updated later on
    permission_classes = [AllowAny]

#class based views to show the detail of a single object
class FaqDetail(generics.RetrieveUpdateDestroyAPIView):
    #f1 = FAQ.objects.create(question="Are you ready?", answer="Yes my guy")
    #f1.save()
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]

class DocListCreate(generics.ListCreateAPIView):
    #resource1 = RESOURCE_METADATA.objects.create(question="Are you ready?", answer="Yes my guy")
    #resource1.save()
    queryset = RESOURCE_METADATA.objects.all()
    serializer_class = DocSerializer
    permission_classes = [AllowAny]
	
class ReportListCreate(generics.ListCreateAPIView):
    #resource1 = RESOURCE_METADATA.objects.create(question="Are you ready?", answer="Yes my guy")
    #resource1.save()
    queryset = RESOURCE_REPORT.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]
	
class UserListCreate(generics.ListCreateAPIView):
    #resource1 = RESOURCE_METADATA.objects.create(question="Are you ready?", answer="Yes my guy")
    #resource1.save()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
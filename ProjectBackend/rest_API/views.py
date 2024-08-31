from django.shortcuts import render
from rest_framework import generics

from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA
from resource_report.models import RESOURCE_REPORT
from django.contrib.auth.models import User, auth

from .serializers import FaqSerializer, DocSerializer, ReportSerializer, UserSerializer
from rest_framework.permissions import AllowAny

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

#to make sure only authorised users has access to api - will be added to permission_classes later on
from rest_framework.permissions import IsAuthenticated

#SERIALIZE DATA - Backend to Frontend
#class based views to show the detail of all objects that are serialized
class FaqListCreate(generics.ListCreateAPIView):
    #f1 = FAQ.objects.create(question="Are you ready?", answer="Yes my guy")
    #f1.save()
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
	#who can get access to the objects, will be updated later on
    permission_classes = [AllowAny]

#class based views to show the detail of a single object that are serialized
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
	
#DESERIALIZE DATA - Frontend to Backend
#class based views to show the detail of all objects that are deserialized
class FaqCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FaqSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the faq instance
            faq = serializer.save()
            # Optionally, return a response with the created user data
            return Response(FaqSerializer(faq).data, status=status.HTTP_201_CREATED)
        else:
            # Return errors if validation fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

	
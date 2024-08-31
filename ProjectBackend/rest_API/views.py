from django.shortcuts import render
from rest_framework import generics

#models
from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA
from resource_report.models import RESOURCE_REPORT
from django.contrib.auth.models import User, auth

#serializing imports
from .serializers import FaqSerializer, DocSerializer, ReportSerializer, UserSerializer

#permissions
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated #must be added later on to allow only authorised users in permission_classes


#deserializing imports
from rest_framework.parsers import JSONParser
from io import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.views import View
from django.http import JsonResponse
from rest_framework import status

#class based views to show the detail of all objects that are serialized

#SERIALIZE DATA CLASSBASED VIEWS - Backend to Frontend
class serializeFaq(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]

class serializeResource(generics.ListCreateAPIView):
    queryset = RESOURCE_METADATA.objects.all()
    serializer_class = DocSerializer
    permission_classes = [AllowAny]
	
class serializeReport(generics.ListCreateAPIView):
    queryset = RESOURCE_REPORT.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]
	
class serializeUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
	
#DESERIALIZE DATA CLASSBASED VIEWS - Frontend to Backend
class deserializeFaq(View):
    def get(request, *args, **kwargs):
        # Example hardcoded JSON object
        json_data = {
            "question": "What is your name?",
            "answer": "My name is mr Test."
        }
        # Convert JSON data to Python dictionary
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        
        # Initialize the serializer with data
        serializer = FaqSerializer(data=data)
        
        if serializer.is_valid():
            # Save the instance and return a response
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeResource(View):
    def get(request, *args, **kwargs):
        # Example hardcoded JSON object
        json_data = {
            "question": "What is your name?",
            "answer": "My name is mr Test."
        }
        # Convert JSON data to Python dictionary
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        
        # Initialize the serializer with data
        serializer = FaqSerializer(data=data)
        
        if serializer.is_valid():
            # Save the instance and return a response
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeReport(View):
    def get(request, *args, **kwargs):
        # Example hardcoded JSON object
        json_data = {
            "question": "What is your name?",
            "answer": "My name is mr Test."
        }
        # Convert JSON data to Python dictionary
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        
        # Initialize the serializer with data
        serializer = FaqSerializer(data=data)
        
        if serializer.is_valid():
            # Save the instance and return a response
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeUser(View):
    def get(request, *args, **kwargs):
        # Example hardcoded JSON object
        json_data = {
            "question": "What is your name?",
            "answer": "My name is mr Test."
        }
        # Convert JSON data to Python dictionary
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        
        # Initialize the serializer with data
        serializer = FaqSerializer(data=data)
        
        if serializer.is_valid():
            # Save the instance and return a response
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)



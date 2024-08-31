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
from rest_framework.views import APIView
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
#WITH TEST DATA
class deserializeFaq(APIView):
    permission_classes = [AllowAny] #remove once login functionality has been completed
    #when a form method/action is "GET"
    def get(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = FaqSerializer(data=data)
        
        if serializer.is_valid():
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

    #when a form method/action is "POST"
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = FaqSerializer(data=data)
        if serializer.is_valid():
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

    #when a form method/action is "PUT"
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            faq_instance = FAQ.objects.get(id=kwargs.get('pk'))
        except FAQ.DoesNotExist:
            return JsonResponse({"error": "FAQ not found."}, status=404)

        serializer = FaqSerializer(faq_instance, data=data, partial=True)
        if serializer.is_valid():
            faq_instance.question = "Alright"
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

    #when a form method/action is "DELETE"
    def delete(self, request, *args, **kwargs):
        try:
            faq_instance = FAQ.objects.get(id=kwargs.get('pk'))
            faq_instance.delete()
            return JsonResponse({"message": "FAQ deleted successfully."}, status=204)
        except FAQ.DoesNotExist:
            return JsonResponse({"error": "FAQ not found."}, status=404)

class deserializeResource(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        json_data = {
            "file_path": "No/path",
            "file_type": "jpg",
            "contributor": "Jesica-System Admin",
            "resource_name": "How to study better",
            "subject": "Study Techniques",
            "grade": "11",
            "keywords": "sociology, sind, research",
            "date_contributed": "2024-08-31T08:26:19.777069Z",
            "resource_rating": 4,
            "approval_status": "Approved",
            "moderation_comment": "This will be very helpful to students",
            "moderation_date": "2024-08-31T10:18:00Z"
        }
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        serializer = DocSerializer(data=data)
        
        if serializer.is_valid():
            resource_instance = serializer.save()
            response_data = {
                "id": resource_instance.id,
                "file_path": resource_instance.file_path ,
                "file_type": resource_instance.file_type,
                "contributor": resource_instance.contributor,
                "resource_name": resource_instance.resource_name,
                "subject": resource_instance.subject,
                "grade": resource_instance.grade,
                "keywords": resource_instance.keywords,
                "date_contributed": resource_instance.date_contributed,
                "resource_rating": resource_instance.resource_rating,
                "approval_status": resource_instance.approval_status,
                "moderation_comment": resource_instance.moderation_comment,
                "moderation_date": resource_instance.moderation_date
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeReport(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        json_data = {
            "reportComplaint": "This is not helpful at all. It distracts my kids from really studying",
            "reportDatetime": "2024-08-31T08:36:56.833338Z",
            "reportResource": "ForeignKeyToResource"
        }
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        serializer = ReportSerializer(data=data)
        
        if serializer.is_valid():
            report_instance = serializer.save()
            response_data = {
                "id": report_instance.id,
                "reportComplaint": report_instance.reportComplaint,
                "reportDatetime": report_instance.reportDatetime,
                "reportResource": report_instance.reportResource
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeUser(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        json_data = {
            "username": "testuser3",
            "email": "testuser@example.com",
            "password": "securepassword"
        }
        json_bytes = JSONRenderer().render(json_data)
        stream = BytesIO(json_bytes)
        data = JSONParser().parse(stream)
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user_instance = serializer.save()
            response_data = {
                "id": user_instance.id,
                "username": user_instance.username,
                "email": user_instance.email
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

#WITHOUT TEST DATA and without allowing everyone access, need authentication and authorisation
"""
class deserializeFaq(APIView):
    def get(self, request, *args, **kwargs):
        json_data = {
            "id": 1,
            "question": "Are you ready?",
            "answer": "Yes my guy"
        }
        data = JSONParser().parse(request)
        serializer = FaqSerializer(data=data)
        
        if serializer.is_valid():
            faq_instance = serializer.save()
            response_data = {
                "id": faq_instance.id,
                "question": faq_instance.question,
                "answer": faq_instance.answer
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeResource(APIView):
    def get(self, request, *args, **kwargs):
        json_data = {
            "file_type": "jpg",
            "contributor": "Jesica-System Admin",
            "resource_name": "How to study better",
            "subject": "Study Techniques",
            "grade": "11",
            "keywords": "sociology, sind, research",
            "date_contributed": "2024-08-31T08:26:19.777069Z",
            "resource_rating": 4,
            "approval_status": "Approved",
            "moderation_comment": "This will be very helpful to students",
            "moderation_date": "2024-08-31T10:18:00Z"
        }
        data = JSONParser().parse(request)
        serializer = DocSerializer(data=data)
        
        if serializer.is_valid():
            resource_instance = serializer.save()
            response_data = {
                "id": resource_instance.id,
                "file_type": resource_instance.file_type,
                "contributor": resource_instance.contributor,
                "resource_name": resource_instance.resource_name,
                "subject": resource_instance.subject,
                "grade": resource_instance.grade,
                "keywords": resource_instance.keywords,
                "date_contributed": resource_instance.date_contributed,
                "resource_rating": resource_instance.resource_rating,
                "approval_status": resource_instance.approval_status,
                "moderation_comment": resource_instance.moderation_comment,
                "moderation_date": resource_instance.moderation_date
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeReport(APIView):
    def get(self, request, *args, **kwargs):
        json_data = {
            "reportComplaint": "This is not helpful at all. It distracts my kids from really studying",
            "reportDatetime": "2024-08-31T08:36:56.833338Z",
            "reportResource": "ForeignKeyToResource"
        }
        data = JSONParser().parse(request)
        serializer = ReportSerializer(data=data)
        
        if serializer.is_valid():
            report_instance = serializer.save()
            response_data = {
                "id": report_instance.id,
                "reportComplaint": report_instance.reportComplaint,
                "reportDatetime": report_instance.reportDatetime,
                "reportResource": report_instance.reportResource
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)

class deserializeUser(APIView):
    def get(self, request, *args, **kwargs):
        json_data = {
            "username": "testuser3",
            "email": "testuser@example.com",
            "password": "securepassword"
        }
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user_instance = serializer.save()
            response_data = {
                "id": user_instance.id,
                "username": user_instance.username,
                "email": user_instance.email
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)
"""
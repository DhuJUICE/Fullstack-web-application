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

#SERIALIZE DATA CLASSBASED VIEWS - Backend making the data available to be used by the frontend
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
	
#DESERIALIZE DATA CLASSBASED VIEWS - Frontend to Backend communication
#WITH TEST DATA
class deserializeFaq(APIView):
    permission_classes = [AllowAny] #remove once login functionality has been completed
    #when a form method/action is "GET"
    #to get a specic object according its primary key id
    def get(self, request, *args, **kwargs):
        faq_id = kwargs.get('pk')
        try:
            faq_instance = FAQ.objects.get(id=faq_id)
            serializer = FaqSerializer(faq_instance)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return JsonResponse({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

    # POST request
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = FaqSerializer(data=data)
        if serializer.is_valid():
            faq_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # PUT request
    def put(self, request, *args, **kwargs):
        faq_id = kwargs.get('pk')
        data = request.data
        try:
            faq_instance = FAQ.objects.get(id=faq_id)
        except FAQ.DoesNotExist:
            return JsonResponse({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FaqSerializer(faq_instance, data=data, partial=True)
        if serializer.is_valid():
            faq_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    def delete(self, request, *args, **kwargs):
        faq_id = kwargs.get('pk')
        try:
            faq_instance = FAQ.objects.get(id=faq_id)
            faq_instance.delete()
            return JsonResponse({"message": "FAQ deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FAQ.DoesNotExist:
            return JsonResponse({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

class deserializeResource(APIView):
    permission_classes = [AllowAny]
    #to get a specic object according its primary key id
    def get(self, request, *args, **kwargs):
        resource_id = kwargs.get('pk')
        try:
            resource_instance = RESOURCE_METADATA.objects.get(id=resource_id)
            serializer = DocSerializer(resource_instance)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except RESOURCE_METADATA.DoesNotExist:
            return JsonResponse({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

    # POST request
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = DocSerializer(data=data)
        if serializer.is_valid():
            resource_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # PUT request
    def put(self, request, *args, **kwargs):
        resource_id = kwargs.get('pk')
        data = request.data
        try:
            resource_instance = RESOURCE_METADATA.objects.get(id=faq_id)
        except RESOURCE_METADATA.DoesNotExist:
            return JsonResponse({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocSerializer(faq_instance, data=data, partial=True)
        if serializer.is_valid():
            resource_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    def delete(self, request, *args, **kwargs):
        resource_id = kwargs.get('pk')
        try:
            resource_instance = RESOURCE_METADATA.objects.get(id=resource_id)
            resource_instance.delete()
            return JsonResponse({"message": "Resource deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except RESOURCE_METADATA.DoesNotExist:
            return JsonResponse({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)


class deserializeReport(APIView):
    permission_classes = [AllowAny]
    #to get a specic object according its primary key id
    def get(self, request, *args, **kwargs):
        report_id = kwargs.get('pk')
        try:
            report_instance = RESOURCE_REPORT.objects.get(id=report_id)
            serializer = ReportSerializer(report_instance)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except RESOURCE_REPORT.DoesNotExist:
            return JsonResponse({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

    # POST request
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            report_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # PUT request
    def put(self, request, *args, **kwargs):
        report_id = kwargs.get('pk')
        data = request.data
        try:
            report_instance = RESOURCE_REPORT.objects.get(id=report_id)
        except RESOURCE_REPORT.DoesNotExist:
            return JsonResponse({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReportSerializer(report_instance, data=data, partial=True)
        if serializer.is_valid():
            report_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    def delete(self, request, *args, **kwargs):
        report_id = kwargs.get('pk')
        try:
            resource_instance = RESOURCE_REPORT.objects.get(id=report_id)
            resource_instance.delete()
            return JsonResponse({"message": "Report deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except RESOURCE_REPORT.DoesNotExist:
            return JsonResponse({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

class deserializeUser(APIView):
    permission_classes = [AllowAny]
    #to get a specic object according its primary key id
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user_instance = User.objects.get(id=user_id)
            serializer = UserSerializer(user_instance)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # POST request
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # PUT request
    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        data = request.data
        try:
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocSerializer(user_instance, data=data, partial=True)
        if serializer.is_valid():
            user_instance = serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user_instance = User.objects.get(id=user_id)
            user_instance.delete()
            return JsonResponse({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


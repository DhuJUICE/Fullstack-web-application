from django.shortcuts import render
from rest_framework import generics

#permissions
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated #must be added later on to allow only authorised users in permission_classes

#models
from faq.models import FAQ
from django.contrib.auth.models import User, auth
from resource_report.models import RESOURCE_REPORT
from resource_contribution.models import RESOURCE_METADATA

#serializing imports
from .serializers import FaqSerializer, DocSerializer, ReportSerializer, UserSerializer

#deserializing imports
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from io import BytesIO

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
	
#DESERIALIZE DATA CLASSBASED VIEWS(Uses serializers) - Frontend to Backend
#WITH TEST DATA
class deserializeFaq(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrieve a single FAQ instance
            try:
                faq = FAQ.objects.get(pk=kwargs['pk'])
                serializer = FaqSerializer(faq)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except FAQ.DoesNotExist:
                return Response({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all FAQ instances
            faqs = FAQ.objects.all()
            serializer = FaqSerializer(faqs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FaqSerializer(data=request.data)
        if serializer.is_valid():
            faq = serializer.save()
            response_data = {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            faq = FAQ.objects.get(pk=kwargs['pk'])
        except FAQ.DoesNotExist:
            return Response({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FaqSerializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            faq = serializer.save()
            response_data = {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            faq = FAQ.objects.get(pk=kwargs['pk'])
            faq.delete()
            return Response({"message": "FAQ deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FAQ.DoesNotExist:
            return Response({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)


class deserializeResource(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrieve a single resource instance
            try:
                resource = RESOURCE_METADATA.objects.get(pk=kwargs['pk'])
                serializer = DocSerializer(resource)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except RESOURCE_METADATA.DoesNotExist:
                return Response({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all resource instances
            resources = RESOURCE_METADATA.objects.all()
            serializer = DocSerializer(resources, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DocSerializer(data=request.data)
        if serializer.is_valid():
            resource = serializer.save()
            response_data = {
                "id": resource.id,
                "file_path": resource.file_path,
                "file_type": resource.file_type,
                "contributor": resource.contributor,
                "resource_name": resource.resource_name,
                "subject": resource.subject,
                "grade": resource.grade,
                "keywords": resource.keywords,
                "date_contributed": resource.date_contributed,
                "resource_rating": resource.resource_rating,
                "approval_status": resource.approval_status,
                "moderation_comment": resource.moderation_comment,
                "moderation_date": resource.moderation_date
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            resource = RESOURCE_METADATA.objects.get(pk=kwargs['pk'])
        except RESOURCE_METADATA.DoesNotExist:
            return Response({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            resource = serializer.save()
            response_data = {
                "id": resource.id,
                "file_path": resource.file_path,
                "file_type": resource.file_type,
                "contributor": resource.contributor,
                "resource_name": resource.resource_name,
                "subject": resource.subject,
                "grade": resource.grade,
                "keywords": resource.keywords,
                "date_contributed": resource.date_contributed,
                "resource_rating": resource.resource_rating,
                "approval_status": resource.approval_status,
                "moderation_comment": resource.moderation_comment,
                "moderation_date": resource.moderation_date
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            resource = RESOURCE_METADATA.objects.get(pk=kwargs['pk'])
            resource.delete()
            return Response({"message": "Resource deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except RESOURCE_METADATA.DoesNotExist:
            return Response({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

class deserializeReport(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                report = RESOURCE_REPORT.objects.get(pk=kwargs['pk'])
                serializer = ReportSerializer(report)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except RESOURCE_REPORT.DoesNotExist:
                return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            reports = RESOURCE_REPORT.objects.all()
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        resource_id = request.data.get('reportResource')
        if resource_id:
            try:
                # Check if the resource exists
                RESOURCE_METADATA.objects.get(id=resource_id)
            except RESOURCE_METADATA.DoesNotExist:
                return Response({"error": "Resource not found."}, status=status.HTTP_400_BAD_REQUEST)
        #from here it goes to the serializer
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save()
            response_data = {
                "id": report.id,
                "reportComplaint": report.reportComplaint,
                "reportDatetime": report.reportDatetime,
                "reportResource": report.reportResource.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            report = RESOURCE_REPORT.objects.get(pk=kwargs['pk'])
        except RESOURCE_REPORT.DoesNotExist:
            return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure 'reportResource' is passed as an ID
        if 'reportResource' in request.data:
            resource_id = request.data['reportResource']
            if resource_id:
                try:
                    resource_instance = RESOURCE_METADATA.objects.get(id=resource_id)
                    request.data['reportResource'] = resource_instance
                except RESOURCE_METADATA.DoesNotExist:
                    return Response({"error": "Resource not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Keep the existing resource if not provided
            request.data['reportResource'] = report.reportResource.id

        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            report = serializer.save()
            response_data = {
                "id": report.id,
                "reportComplaint": report.reportComplaint,
                "reportDatetime": report.reportDatetime,
                "reportResource": report.reportResource.id
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        try:
            report = RESOURCE_REPORT.objects.get(pk=kwargs['pk'])
            report.delete()
            return Response({"message": "Report deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except RESOURCE_REPORT.DoesNotExist:
            return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

class deserializeUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # Retrieve a single user instance
            try:
                user = User.objects.get(pk=kwargs['pk'])
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all user instances
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


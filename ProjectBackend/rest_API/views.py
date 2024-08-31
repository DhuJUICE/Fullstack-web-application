from django.shortcuts import render
from rest_framework import generics

from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA

from .serializers import FaqSerializer, DocSerializer
from rest_framework.permissions import AllowAny


class FaqListCreate(generics.ListCreateAPIView):
    #f1 = FAQ.objects.create(question="Are you ready?", answer="Yes my guy")
    #f1.save()
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]

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
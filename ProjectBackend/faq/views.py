from django.shortcuts import render
from rest_framework import generics
from .models import FAQ
from .serializers import FaqSerializer
from rest_framework.permissions import AllowAny

class FaqListCreate(generics.ListCreateAPIView):
    f1 = FAQ.objects.create(question="Are you ready?", answer="Yes my guy")
    f1.save()
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]

class FaqDetail(generics.RetrieveUpdateDestroyAPIView):
    f1 = FAQ.objects.create(question="Are you ready?", answer="Yes my guy")
    f1.save()
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]

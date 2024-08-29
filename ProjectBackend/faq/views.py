from django.shortcuts import render
from rest_framework import generics
from .models import FAQ
from .serializers import FaqSerializer

class FaqListCreate(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer

class FaqDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer

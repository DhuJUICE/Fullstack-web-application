from django.shortcuts import render
from rest_framework import generics
from .models import FAQ
from .serializers import FaqSerializer

class BookListCreate(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FaqSerializer

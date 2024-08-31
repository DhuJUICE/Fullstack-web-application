from rest_framework import serializers
from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA
from resource_report.models import RESOURCE_REPORT
from django.contrib.auth.models import User, auth
from rest_framework.exceptions import ValidationError

#Serializers
class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        
        fields = '__all__'  # or specify fields explicitly
		
class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = RESOURCE_METADATA
        
        fields = '__all__'  # or specify fields explicitly
		
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RESOURCE_REPORT
        
        fields = '__all__'  # or specify fields explicitly
		
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields = '__all__' #specify fields explicitly
		


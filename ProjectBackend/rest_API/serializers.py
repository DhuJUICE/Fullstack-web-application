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
    
    #functions to handle nested relationships between reports and resources    
    def create(self, validated_data):
        resource_data = validated_data.pop('reportResource')
        resource_instance = RESOURCE_METADATA.objects.get(id=resource_data['id'])
        report = RESOURCE_REPORT.objects.create(
            reportResource=resource_instance,
            **validated_data
        )
        return report

    def update(self, instance, validated_data):
        resource_data = validated_data.pop('reportResource')
        instance.reportResource = RESOURCE_METADATA.objects.get(id=resource_data['id'])
        instance.reportComplaint = validated_data.get('reportComplaint', instance.reportComplaint)
        instance.reportDatetime = validated_data.get('reportDatetime', instance.reportDatetime)
        instance.save()
        return instance

		
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields = '__all__' #specify fields explicitly
		


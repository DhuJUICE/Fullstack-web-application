from rest_framework import serializers
from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        
        fields = '__all__'  # or specify fields explicitly
		
class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = RESOURCE_METADATA
        
        fields = '__all__'  # or specify fields explicitly

from rest_framework import serializers
from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA
from user_management.models import UserProfile
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
        #this gets me the object associated with the reportResource that was posted by the user
        resource_instance = validated_data.pop('reportResource')

        #explicitly make the reportResource the above object
        report = RESOURCE_REPORT.objects.create(
            reportResource=resource_instance,
            **validated_data
        )
        #from here it goes back to the views
        return report

    def update(self, instance, validated_data):
        #this is to get the resource object
        instance.reportResource = validated_data.pop('reportResource')

        #this is the information to update about the report object
        instance.reportComplaint = validated_data.get('reportComplaint', instance.reportComplaint)
        
        #we wont need to update the reportDatetime as it is the time the report was first made
        #instance.reportDatetime = validated_data.get('reportDatetime', instance.reportDatetime)

        #save the instance to database
        instance.save()
        return instance

		
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields = '__all__' #specify fields explicitly

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        user = User.objects.create(username=username, password=password, email=email)  # Create the User instance
        
        return user

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)  # Extract user data if provided

        if user_data:
            # Update the user instance
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update the UserProfile instance
        instance.role = validated_data.get('role', instance.role)
        instance.image = validated_data.get('image', instance.image)
        instance.verificationCode = validated_data.get('verificationCode', instance.verificationCode)
        instance.save()
        return instance
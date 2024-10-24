from rest_framework import serializers
from faq.models import FAQ
from resource_contribution.models import RESOURCE_METADATA
from user_management.models import UserProfile
from resource_report.models import RESOURCE_REPORT
from user_analytics.models import ANALYTICS
from django.contrib.auth.models import User, auth
from rest_framework.exceptions import ValidationError

#Serializers
class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ANALYTICS

        fields = '__all__'

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
        fields = '__all__'
        extra_kwargs = {
            'reportUser': {'required': False}  # Allow reportUser to be optional
        }

    def create(self, validated_data):
        # Set reportUser to the current user if not provided
        reportUser = validated_data.pop('reportUser', None)  # If present, pop it

        # Create the report instance
        report = RESOURCE_REPORT.objects.create(
            reportUser=reportUser,  # This should be set in the view, not the request
            **validated_data
        )
        return report

    def update(self, instance, validated_data):
        # Check if reportResource is provided in the data
        if 'reportResource' in validated_data:
            resource_instance = validated_data.pop('reportResource')
            instance.reportResource = resource_instance

        # Update the other fields
        instance.reportComplaint = validated_data.get('reportComplaint', instance.reportComplaint)

        # We won't need to update the reportDatetime as it is auto-set on creation
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

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)  # Make sure to handle password hashing
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        user = User.objects.get(email=email)
        # Update the UserProfile instance
        userProfile = UserProfile.objects.get(user=user)
        userProfile.role = validated_data.get('role', instance.role)
        print(userProfile.role)
        #userProfile.image = validated_data.get('image', instance.image)
        #print(userProfile.image)
        userProfile.save()

        return instance
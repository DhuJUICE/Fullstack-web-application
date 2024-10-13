from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.
class RESOURCE_METADATA(models.Model):

    #Resource Metadata
    #identifier from aws s3
    file_path1 = models.FileField(upload_to='resources/', null=True, blank=True)
    file_path2 = models.FileField(upload_to='resources/', null=True, blank=True)
    file_path3 = models.FileField(upload_to='resources/', null=True, blank=True)
    file_path4 = models.FileField(upload_to='resources/', null=True, blank=True)

    #what type of file is being stored as the resource
    file_type = models.CharField(max_length = 100)
    date_contributed = models.DateTimeField(auto_now_add=True)

    #get the id of the person uploading the resource
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)

    #details about the specific resource
    resource_name = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 100)
    grade = models.CharField(max_length = 100)

    #keywords contains a list of keywords to find the resource with(need an array later on),delimeter will be used
    keywords = models.TextField()
    
    #rating of the resource 1-5
    resource_rating = models.IntegerField(null=True, blank=True)

    APPROVAL_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
    #moderation details
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS_CHOICES, default='pending')
    moderation_comment = models.TextField(null=True, blank=True)
    moderation_date = models.DateTimeField(null=True, blank=True)

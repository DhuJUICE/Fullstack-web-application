from django.db import models
from django.contrib.auth.models import User, auth
# Create your models here.
class RESOURCE_METADATA(models.Model):

    #Resource Metadata
    #identifier from aws s3
    #file_Path = models.FileField(upload_to='aws')

    #what type of file is being stored as the resource
    file_type = models.CharField(max_length = 100)

    #get the id of the person uploading the resource
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)

    #details about the specific resource
    resource_name = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 100)
    grade = models.CharField(max_length = 100)

    #keywords contains a list of keywords to find the resource with(need an array later on)
    keywords = models.CharField(max_length = 100)

    date_contributed = models.DateTimeField(auto_now_add=True)

    #rating of the resource
    resource_rating = models.IntegerField()

    #moderation details
    approval_status = models.CharField(max_length = 100)
    moderation_comment = models.CharField(max_length = 100)
    moderation_date = models.DateTimeField()

from django.db import models

# Create your models here.
class ResourceMetadata(models.Model):

    #resource-metadata
    File_Path = ""
    File_Type = ""
    
    Resource_Name = ""
    Subject = ""
    Grade = ""
    Keywords = ""
    Date_Contributed = ""
    
    Resource_Rating = ""
    
    Approval_Status = ""
    Moderation_Comment = ""
    Moderation_Date = ""
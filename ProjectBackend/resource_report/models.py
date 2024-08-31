from django.db import models
from resource_contribution.models import RESOURCE_METADATA

# Create your models here.
class RESOURCE_REPORT(models.Model):
    #Resource Report
    #reportResource = models.ForeignKey(RESOURCE_METADATA, on_delete=models.CASCADE) #use later
    reportResource = models.CharField(max_length = 100, default="ForeignKeyToResource")
    reportComplaint = models.CharField(max_length = 100)
    reportDatetime = models.DateTimeField(auto_now_add=True)

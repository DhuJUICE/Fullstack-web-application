from django.db import models
from resource_contribution.models import RESOURCE_METADATA

# Create your models here.
class RESOURCE_REPORT(models.Model):
    #Resource Report
    reportResource = models.ForeignKey(RESOURCE_METADATA, on_delete=models.CASCADE)
    reportComplaint = models.CharField(max_length = 100)

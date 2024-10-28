from django.db import models

#User analytics model
class ANALYTICS(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True)  # Unique identifier for the user
    page = models.CharField(max_length=255, null=True, blank=True)      # Title of the page being viewed
    event_type = models.CharField(max_length=50, null=True, blank=True) # Type of interaction ("page_view" etc)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True) 

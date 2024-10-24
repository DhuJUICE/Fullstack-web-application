from django.db import models

#User analytics model
class ANALYTICS(models.Model):
    event_category = models.CharField(max_length = 100, null=True, blank=True)
    event_action = models.CharField(max_length = 100, null=True, blank=True)
    event_label = models.CharField(max_length = 100, null=True, blank=True)
    user_id = models.CharField(max_length = 100, null=True, blank=True)
    event_duration = models.CharField(max_length = 100, null=True, blank=True)
    custom_param = models.CharField(max_length = 100, null=True, blank=True)

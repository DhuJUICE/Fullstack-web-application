from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #options for users as roles
    USER_ROLES_CHOICES = [
    ('openUser', 'Open Access'),
    ('adminUser', 'Admin'),
    ('educatorUser', 'Educator'),
    ('moderatorUser', 'Moderator'),
]
    #moderation details
    role = models.CharField(max_length=20, choices=USER_ROLES_CHOICES, default='openUser')
    image = models.CharField(max_length=100, blank=True, null=True)
    verificationCode = models.CharField(max_length=100, blank=True, null=True)

from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #options for users as roles
    USER_ROLES_CHOICES = [
    #this open access user option is not needed as open access users will only be default
    ('openUser', 'Open Access'),
    #these are the roles that can be applied for
    ('adminUser', 'Admin'),
    ('educatorUser', 'Educator'),
    ('moderatorUser', 'Moderator'),
]
    #User Profile details
    #Acess role
    role = models.CharField(max_length=20, choices=USER_ROLES_CHOICES, default='openUser')
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    verificationCode = models.CharField(max_length=8, blank=True, null=True)
    codeTimestamp = models.DateTimeField(blank=True, null=True)

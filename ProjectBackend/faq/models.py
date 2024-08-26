from django.db import models

# Create your models here.
class FAQ(models.Model):

    #Frequently asked questions and their answers
    question = models.CharField(max_length = 300)
    answer = models.CharField(max_length = 300)

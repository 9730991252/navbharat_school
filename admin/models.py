from django.db import models
from school.models import *
#Create your models here.
class Admin_login(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, related_name='batch')
    mobile = models.IntegerField(unique=True)
    pin = models.IntegerField()
    
class Admin(models.Model):
    name = models.CharField(max_length=100, null=True)
    qualification = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="admin_images",default="",null=True, blank=True)
    about_us = models.CharField(max_length=1000, null=True)
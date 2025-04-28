from django.db import models

# Create your models here.
class web_visitor(models.Model):
    count = models.IntegerField(default=1)
    
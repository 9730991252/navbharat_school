from django.db import models
from school.models import *
# Create your models here.
class Leave_letter(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    added_date = models.DateField(auto_now_add=True, null=True)
    status = models.IntegerField(default=0)  # 0 = pending, 1 = approved, 2 = rejected
    accepted_date = models.DateField(null=True)
    reason = models.TextField()
    
class Student_used_count(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    used_count = models.IntegerField(default=0)
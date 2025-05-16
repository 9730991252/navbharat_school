from django.db import models
from school.models import *
# Create your models here.
Check_in_out_type={
    '1':'auto',
    '0':'manual'
}
class Student_Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    check_in_by_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='check_in_by_teacher')
    check_out_by_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='check_out_by_teacher')
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
    check_in_type = models.IntegerField(default=1, null=True)
    check_out_type = models.IntegerField(default=1, null=True)
    
class Teacher_used_count(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    used_count = models.IntegerField(default=0)
    
class Todayes_teaching(models.Model):
    subject_class_and_teacher = models.ForeignKey(Subject_class_and_teacher, on_delete=models.CASCADE, related_name='subject_class_and_teacher')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='tbatch')
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True)

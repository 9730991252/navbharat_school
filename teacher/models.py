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
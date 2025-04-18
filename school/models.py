from django.db import models
from PIL import Image
# Create your models here.
class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField(default=1)
    edit_status = models.IntegerField(default=1)
    
class Clerk(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='clerks')
    name = models.CharField(max_length=100, unique=True)
    mobile = models.IntegerField(unique=True)
    secret_pin = models.IntegerField()
    status = models.IntegerField(default=1)
    
class Teacher(models.Model):
    clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='clerk')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=100, unique=True)
    mobile = models.IntegerField(unique=True)
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    gender = models.CharField(max_length=10, null=True)
    aadhar_number = models.IntegerField(unique=True,null=True)
    qualification = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="teacher_images",default="",null=True, blank=True)
    added_date = models.DateField(auto_now_add=True, null=True)
    branding_status = models.IntegerField(default=0,null=True)
    about_you = models.TextField(null=True)
    
    
GENDER_CHOICES = (
    ('MALE', "MALE"),
    ('FEMALE', "FEMALE"),
)

class Student(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    aadhar_number = models.IntegerField(unique=True)
    secret_pin = models.CharField(max_length=10)
    status = models.IntegerField(default=1)
    gender = models.CharField(max_length=10)
    added_date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by')
    edit_status = models.IntegerField(default=1)
 
class Student_Image(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="student_images",default="",null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)

class School_class(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)

class Class_student(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    school_class = models.ForeignKey(School_class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
class Class_teacher(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    school_class = models.ForeignKey(School_class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    

class Subject(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)
    
class Subject_class_and_teacher(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(School_class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
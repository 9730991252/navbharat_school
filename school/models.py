from django.db import models

# Create your models here.
# class Batch(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     status = models.IntegerField(default=1)
#     edit_status = models.IntegerField(default=1)
    
# class Clerk(models.Model):
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='clerks')
#     name = models.CharField(max_length=100, unique=True)
#     mobile = models.IntegerField(unique=True)
#     secret_pin = models.IntegerField()
#     status = models.IntegerField(default=1)
    
# class Teacher(models.Model):
#     clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='clerk')
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='teachers')
#     name = models.CharField(max_length=100, unique=True)
#     mobile = models.IntegerField(unique=True)
#     pin = models.IntegerField()
#     status = models.IntegerField(default=1)
#     gender = models.CharField(max_length=10, null=True)

    
    
# GENDER_CHOICES = (
#     ('MALE', "MALE"),
#     ('FEMALE', "FEMALE"),
# )

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     mobile = models.IntegerField()
#     aadhar_number = models.IntegerField(unique=True)
#     secret_pin = models.CharField(max_length=10)
#     status = models.IntegerField(default=1)
#     gender = models.CharField(max_length=10)
#     added_date = models.DateField(auto_now_add=True)
#     added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by')
#     edit_status = models.IntegerField(default=1)
 
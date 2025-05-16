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
    address = models.CharField(max_length=255, null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by')
    edit_status = models.IntegerField(default=1)
    tocken = models.CharField(max_length=1000, null=True, blank=True)
    date_of_birth = models.DateField(null=True)

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

class Holidays(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateField(null=True)
    reason = models.CharField(max_length=100,null=True)

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
    
class Notice(models.Model):
    notice_number = models.CharField(max_length=100,null=True)
    by_clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='by_clerk')
    by_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='by_teacher')
    by_admin = models.IntegerField(default=0)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, related_name='batches')    
    to_class = models.ForeignKey(School_class, on_delete=models.CASCADE, null=True, related_name='to_class')
    to_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='to_student')
    to_school = models.IntegerField(default=0)
    to_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='to_teacher')
    to_all_teachers = models.IntegerField(default=0)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)
    
class Readed_Notice(models.Model):
    read_by_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='read_by_student')
    read_by_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='read_bby_teacher')
    read_by_admin = models.IntegerField(default=0)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True, related_name='read_by_notice')
    readed_date = models.DateTimeField(auto_now_add=True, null=True)
    
class Bank_Account(models.Model):
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True)
    account_number = models.CharField(max_length=100, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    status = models.IntegerField(default=1)
    
class Clerk_used_count(models.Model):
    clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE)
    used_count = models.IntegerField(default=0)

    
class Student_received_Fee_Cash(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    received_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_received_fee')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student_received_fee')

class Student_recived_Fee_Bank(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    recived_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_student_recived_fee')
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_student_recived_fee')
    account = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True, blank=True)
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    utr_number = models.CharField(max_length=100, null=True, blank=True)
    
class Cash_Transfer_To_Bank(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    from_admin = models.IntegerField(default=0)
    from_clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, blank=True)
    to_bank = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0)
    transfer_date = models.DateField(null=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(null=True)
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)

class Cash_Transfer_To_Admin(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    from_clerk = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0)
    transfer_date = models.DateField(null=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(null=True)
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)
    
class Expenses(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    remark = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    added_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='added_by_clerk')
    from_bank = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=True, blank=True, related_name='from_bank')
    check_number = models.CharField(max_length=100,null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=True)
    updated_by = models.ForeignKey(Clerk, on_delete=models.CASCADE, null=True, related_name='updated_by_clerk')
    updated_date = models.DateTimeField(null=True)
    admin_verify_status = models.IntegerField(default=0) # 0 = not verify, 1 = verify
    verify_date = models.DateTimeField(null=True, blank=True)


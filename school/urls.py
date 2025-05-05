from django.urls import path
from . import views

urlpatterns = [
    path('school_home/', views.school_home, name='school_home'),
    
    #teacher
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    
    #student
    path('add_student/', views.add_student, name='add_student'),
    
    #class
    path('add_class/', views.add_class, name='add_class'),
    path('select_student_class/', views.select_student_class, name='select_student_class'),
    path('select_student_class/<id>/', views.select_student_class_id, name='select_student_class'),
    path('select_class_teacher/', views.select_class_teacher, name='select_class_teacher'),
    
    #subject
    path('add_subject/', views.add_subject, name='add_subject'),
    path('select_subject_class_and_teacher/', views.select_subject_class_and_teacher, name='select_subject_class_and_teacher'),
    path('student_image/', views.student_image, name='student_image'),
    
    #holidays
    path('holidays/', views.holidays, name='holidays'),
    
    #account
    path('add_bank_account/', views.add_bank_account, name='add_bank_account'),
    path('student_fees/', views.student_fees, name='student_fees'),
    path('student_fee_detail/<id>', views.student_fee_detail, name='student_fee_detail'),
    path('school_cash_transfer/', views.school_cash_transfer, name='school_cash_transfer'),
    path('school_expenses/', views.school_expenses, name='school_expenses'),
]
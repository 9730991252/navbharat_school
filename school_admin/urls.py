from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/',                 views.admin_home,               name='admin_home'),
    path('admin_view_students/',        views.admin_view_students,      name='admin_view_students'),
    path('admin_view_teacher/',         views.admin_view_teacher,       name='admin_view_teacher'),
    path('todayes_attendence/',         views.todayes_attendence,       name='todayes_attendence'),
    path('admin_notice/',               views.admin_notice,             name='admin_notice'),
    path('admin_school_notice/',        views.admin_school_notice,      name='admin_school_notice'),
    path('admin_class_notice/',         views.admin_class_notice,       name='admin_class_notice'),
    path('admin_teacher_notice/',       views.admin_teacher_notice,     name='admin_teacher_notice'),
    path('admin_student_notice/',       views.admin_student_notice,     name='admin_student_notice'),
    path('admin_received_notice/',      views.admin_received_notice,    name='admin_received_notice'),
    path('admin_account/',              views.admin_account,            name='admin_account'),
    path('credit/',                     views.credit,                   name='credit'),
    path('debit/',                      views.debit,                    name='debit'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('attendance/', views.attendance, name='attendance'),
    path('student_check_in/', views.student_check_in, name='student_check_in'),
    path('profile/', views.profile, name='profile'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('attendance/', views.attendance, name='attendance'),
    path('student_check_in/', views.student_check_in, name='student_check_in'),
    path('student_check_out/', views.student_check_out, name='student_check_out'),
    path('profile/', views.profile, name='profile'),
    path('video_feed_check_in/', views.video_feed_check_in, name='video_feed_check_in'),
    path('video_feed_check_out/', views.video_feed_check_out, name='video_feed_check_out'),
    path('student_leaves/', views.student_leaves, name='student_leaves'),
    path('students_icard_for_teacher/', views.students_icard_for_teacher, name='students_icard_for_teacher'),
    path('teacher_notice/', views.teacher_notice, name='teacher_notice'),
    path('teacher_received_notice/', views.teacher_received_notice, name='teacher_received_notice'),
    
]
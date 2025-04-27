from django.urls import path
from . import views
urlpatterns = [
    path('search_student/', views.search_student, name='search_student'),
    path('select_student/', views.select_student, name='select_student'),
    path('search_student_image/', views.search_student_image, name='search_student_image'),
    path('search_student_for_check_in/', views.search_student_for_check_in, name='search_student_for_check_in'),
    path('check_in_student_manual/', views.check_in_student_manual, name='check_in_student_manual'),
    path('search_student_for_check_out/', views.search_student_for_check_out, name='search_student_for_check_out'),
    path('check_out_student_manual/', views.check_out_student_manual, name='check_out_student_manual'),
    path('search_attrndance_day/', views.search_attrndance_day, name='search_attrndance_day'),
    path('search_holiday/', views.search_holiday, name='search_holiday'),
    path('check_day/', views.check_day, name='check_day'),
    path('search_student_for_edit/', views.search_student_for_edit, name='search_student_for_edit'),
    path('save_readed_notices_student/', views.save_readed_notices_student, name='save_readed_notices_student'),
    path('save_readed_notices_admin/', views.save_readed_notices_admin, name='save_readed_notices_admin'),
    path('save_readed_notices_teacher/', views.save_readed_notices_teacher, name='save_readed_notices_teacher'),
]
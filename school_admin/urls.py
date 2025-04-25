from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_view_students/', views.admin_view_students, name='admin_view_students'),
    path('admin_view_teacher/', views.admin_view_teacher, name='admin_view_teacher'),
    path('todayes_attendence/', views.todayes_attendence, name='todayes_attendence'),
    path('admin_notice/', views.admin_notice, name='admin_notice'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('school_home/', views.school_home, name='school_home'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('add_student/', views.add_student, name='add_student'),
]
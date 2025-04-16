from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('school_login/', views.school_login, name='school_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('parent_login/', views.parent_login, name='parent_login'),
    path('teacher_login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout, name='logout'),
]
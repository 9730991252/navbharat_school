from django.urls import path
from . import views
urlpatterns = [
    path('search_student/', views.search_student, name='search_student'),
    path('select_student/', views.select_student, name='select_student'),
    path('search_student_image/', views.search_student_image, name='search_student_image'),
]
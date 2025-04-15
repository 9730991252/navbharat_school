from django.urls import path
from . import views

urlpatterns = [
    path('face-attendance/', views.face_attendance_view, name='face_attendance'),
    path('start-attendance/', views.start_attendance, name='start_attendance'),
]

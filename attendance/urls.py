from django.urls import path
from . import views

urlpatterns = [
    path('face/', views.face_attendance_view, name='face_attendance'),
    path('process-frame/', views.process_frame, name='process-frame'),
]

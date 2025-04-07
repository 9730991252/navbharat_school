from django.urls import path
from . import views

urlpatterns = [
    path('student_home/<batch_id>', views.student_home, name='student_home'),
    path('notice/<batch_id>', views.notice, name='notice'),
    path('videos/<batch_id>', views.videos, name='notice'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('student_home/<batch_id>', views.student_home, name='student_home'),
    path('notice/<batch_id>', views.notice, name='notice'),
    path('videos/<batch_id>', views.videos, name='notice'),
    path('student_profile/<batch_id>', views.student_profile, name='student_profile'),
    path('leave_letter/<batch_id>', views.leave_letter, name='leave_letter'),
    path('save-token/', views.save_token, name='save-token'),
]
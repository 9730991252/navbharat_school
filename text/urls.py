
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save-token/', views.save_token, name='save_token'),
    path('send-push/', views.send_push, name='send_push'),
    path('delete/', views.delete, name='delete'),
]
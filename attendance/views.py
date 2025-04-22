import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
from django.shortcuts import render
from django.http import JsonResponse
from school.models import *
from teacher.models import *
# Load student images from the database
def face_attendance_view(request):
    window = cv2.VideoCapture(0)
    while True:
        success, frame = window.read()
        if not success:
            break
        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        cv2.imshow('Face Recognition Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    window.release()
    cv2.destroyAllWindows()
    return render(request, 'face_attendance.html')
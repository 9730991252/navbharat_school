import cv2
import numpy as np
import face_recognition
import json
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from school.models import Student_Image
from teacher.models import *
import base64
from io import BytesIO
from PIL import Image

def face_attendance_view(request):
    student_data = []
    for s in Student_Image.objects.all():
        try:
            image = face_recognition.load_image_file(s.image.path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                student_data.append({
                    'id': s.student.id,
                    'name': s.student.name,
                    'encoding': encodings[0].tolist(),  # Convert numpy array to list
                })
        except Exception as e:
            print(f"Error loading image for {s.student.name}: {e}")
            continue
    students_json = json.dumps(student_data)
    return render(request, 'face_attendance.html', {'students_json': students_json})

@csrf_exempt
def process_frame(request):
    if request.method == 'POST' and request.FILES.get('frame'):
        frame_file = request.FILES['frame']
        students_json = request.POST.get('students')
        students = json.loads(students_json)

        frame_data = np.asarray(bytearray(frame_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        today = date.today()
        for face_encoding in face_encodings:
            distances = [face_recognition.face_distance([np.array(s['encoding'])], face_encoding)[0] for s in students]
            if distances and min(distances) <= 0.45:
                idx = np.argmin(distances)
                student = students[idx]

                # Mark attendance if not already marked
                already_marked = Student_Attendance.objects.filter(
                    student_id=student['id'],
                    check_in__date=today
                ).exists()
                if not already_marked:
                    Student_Attendance.objects.create(student_id=student['id'], check_in=today)

                # Return image from disk (reload for safety)
                try:
                    student_image_obj = Student_Image.objects.get(student_id=student['id'])
                    image = cv2.imread(student_image_obj.image.path)
                    image = cv2.resize(image, (150, 150))
                    _, buffer = cv2.imencode('.jpg', image)
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    return JsonResponse({
                        'status': 'matched',
                        'name': student['name'],
                        'image': img_base64
                    })
                except:
                    return JsonResponse({'status': 'matched', 'name': student['name'], 'image': None})

        return JsonResponse({'status': 'no match'})  # Unknown
    return JsonResponse({'error': 'Invalid request'}, status=400)
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
def load_student_images_from_db():
    images = []
    student_names = []
    students = Student.objects.all()
    
    for student in students:
        student_image = Student_Image.objects.filter(student=student).first()  # Get the first image for the student
        
        if student_image and student_image.image:
            img_path = student_image.image.path  # Get image path from the database
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
                student_names.append(student.name)  # Assuming `name` is the field in the `Student` model
    
    return images, student_names

def findEncodings(images):
    encode_list = []
    for img in images:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        if encodings:
            encode_list.append(encodings[0])
    return encode_list

# View for the face attendance page
def face_attendance_view(request):
    return render(request, 'face_attendance.html')

# AJAX endpoint to handle face recognition process
def start_attendance(request):
    cap = cv2.VideoCapture(0)
    marked_names = set()

    # Create CSV file for attendance logging
    now = datetime.now()
    csv_filename = f'{now.strftime("%Y-%m-%d_%H-%M-%S")}_attendance.csv'
    csv_file = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Name", "Time"])

    # Assuming we have Clerk and Teacher data to log attendance properly
    clerk = Clerk.objects.first()  # Modify to get actual Clerk data
    teacher = Teacher.objects.first()  # Modify to get actual Teacher data

    # Load student images and encodings from the database
    images, student_names = load_student_images_from_db()
    known_encodings = findEncodings(images)
    known_names = student_names.copy()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for encoding, face_loc in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            face_distances = face_recognition.face_distance(known_encodings, encoding)

            name = "Unknown"
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            if name != "Unknown" and name not in marked_names:
                time_now = datetime.now().strftime("%H:%M:%S")
                csv_writer.writerow([name, time_now])
                marked_names.add(name)
                print(f"[✓] Marked Present: {name} at {time_now}")

                # Get the student object by the matched name
                try:
                    student = Student.objects.get(name=name)

                    # Save image if it's a valid student
                    student_image = Student_Image(
                        student=student,
                        image=student_image.image,  # Assuming `image` is the field in the `Student_Image` model
                        added_by=clerk,  # Assuming Clerk object is available
                    )
                    student_image.save()

                    # Create attendance entry
                    attendance = Student_Attendance(
                        student=student,
                        check_in_by_teacher=teacher,  # Assuming Teacher object is available
                        check_in=datetime.now(),
                        check_in_type=1,  # Auto check-in
                    )
                    attendance.save()

                except Student.DoesNotExist:
                    print(f"Student {name} not found in the database.")

            # Draw box and name (optional, for visual feedback)
            top, right, bottom, left = [v * 4 for v in face_loc]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Send frame to frontend (can be converted to base64 and sent as a response)

    # Cleanup
    csv_file.close()
    cap.release()
    cv2.destroyAllWindows()
    
    return JsonResponse({"status": "Attendance completed", "csv_filename": csv_filename})

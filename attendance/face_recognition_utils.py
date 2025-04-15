import face_recognition
from school.models import *
from teacher.models import *

def load_student_faces():
    known_face_encodings = []
    known_face_ids = []

    students_images = Student_Image.objects.all()

    for student_image in students_images:
        image = face_recognition.load_image_file(student_image.image.path)
        face_encoding = face_recognition.face_encodings(image)

        if face_encoding:
            known_face_encodings.append(face_encoding[0])
            known_face_ids.append(student_image.student.id)

    return known_face_encodings, known_face_ids

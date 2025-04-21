from navbharat_school.includes import *

def generate_frames_check_in(request):
    mobile = request.session['teacher_mobile']
    teacher = Teacher.objects.filter(mobile=mobile).first()
    video = cv2.VideoCapture(0)

    known_faces = []
    for student in Student_Image.objects.all():
        try:
            img = cv2.imread(student.image.path)
            if img is None:
                continue
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                known_faces.append({
                    'id': student.student.id,
                    'name': student.student.name,
                    'encoding': encodings[0],
                    'image': img
                })
        except Exception as e:
            print(f"Error processing {student.student.name}: {e}")
            continue

    last_matched_image = None
    last_display_name = "No Match Yet"

    while True:
        success, frame = video.read()
        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            known_encodings = [entry['encoding'] for entry in known_faces]
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            text = ''
            if face_distances.any():
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    matched_student = known_faces[best_match_index]
                    student_id = matched_student['id']
                    text = matched_student['name']
                    already = Student_Attendance.objects.filter(student_id=student_id).first()
                    if not already:
                        Student_Attendance(
                            student_id=student_id,
                            check_in_by_teacher=teacher,
                            check_in=datetime.now(),
                        ).save()
                    else:
                        a =Student_Attendance.objects.all().last() 
                        if a.student_id != student_id:
                            text = f"{matched_student['name']} Already Exists"
                    # Save last matched info
                    last_matched_image = matched_student['image']
                    last_display_name = text
                    top, right, bottom, left = face_location
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, text, (left, top - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Display matched student image on screen
        if last_matched_image is not None:
            try:
                thumb = cv2.resize(last_matched_image, (150, 150))
                h, w, _ = thumb.shape
                # place image in top-right corner
                frame[10:10+h, frame.shape[1]-w-10:frame.shape[1]-10] = thumb
                # draw name below thumbnail
                cv2.putText(frame, last_display_name,
                            (frame.shape[1]-w-10, 10+h+25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            except Exception as e:
                print(f"Error displaying thumbnail: {e}")

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    video.release()
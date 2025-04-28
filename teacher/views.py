from navbharat_school.includes import *

# Create your views here.
def teacher_home(request):
    Student_Image.objects.all().delete()
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        class_students_count = 0
        teacher = Teacher.objects.filter(mobile=mobile).first()
        teacher_class = Class_teacher.objects.filter(teacher=teacher).first()
        if teacher_class:
            class_students = Class_student.objects.filter(school_class=teacher_class.school_class)
            class_students_count = class_students.count()
        messages.success(request, 'Welcome to NAVBHARAT ENGLISH MEDIUM SCHOOL KARMALA!')
        
        
        context={
            'teacher':teacher,
            'teacher_class':teacher_class,
            'class_teacher_subject':Subject_class_and_teacher.objects.filter(school_class=teacher_class.school_class,teacher=teacher).first() if teacher_class else 'None',
            'class_students_count':class_students_count ,
            'subject_class_and_teacher':Subject_class_and_teacher.objects.filter(teacher=teacher)
        }
        return render(request, 'teacher_home.html', context)
    else:
        return redirect('school_mobile')
    
@csrf_exempt
def profile(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        if 'add_image'in request.POST:
            img_data = request.POST.get('img')  # base64 string

            format, imgstr = img_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{id}.{ext}')
            
            if teacher.image != None:
                if teacher.image:
                    old_image_path = teacher.image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
            teacher.image.save(f'{teacher.name}.webp', data, save=True)
            messages.success(request, f'Image Added Successfully Ms/Miss.{teacher.name}')
            return redirect('/teacher/profile/')
        if 'add_about_info'in request.POST:
            teacher.about_you = request.POST.get('about_you')
            teacher.save()
            messages.success(request, f'Information saved Successfully Ms/Miss.{teacher.name}')
            return redirect('/teacher/profile/')
            
        context={
            'teacher':teacher,
        }
        return render(request, 'teacher_profile.html', context)
    else:
        return redirect('school_mobile')
    
def attendance(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        classes = []
        for c in School_class.objects.filter(batch=teacher.batch, status=1):
            check_ins = 0
            check_outs = 0
            list =[]
            for c_in in Student_Attendance.objects.filter(check_in__date=now().date()):
                stc = Class_student.objects.filter(student_id=c_in.student.id).first()
                if stc != None:
                    if stc.school_class == c:
                        check_ins += 1
                        list.append({
                            'student':c_in.student,
                            'check_in_by_teacher':c_in.check_in_by_teacher,
                            'check_out_by_teacher':c_in.check_out_by_teacher,
                            'check_in':c_in.check_in,
                            'check_out':c_in.check_out,
                            'check_in_type':c_in.check_in_type,
                            'check_out_type':c_in.check_out_type,
                        })
            for c_out in Student_Attendance.objects.filter(check_out__date=now().date()):
                stc = Class_student.objects.filter(student_id=c_out.student.id).first()
                if stc != None:
                    if stc.school_class == c:
                        check_outs += 1
            classes.append({
                'id':c.id,
                'name':c.name,
                'check_ins':check_ins,
                'check_outs':check_outs,
                'list':list
            })
        context={
            'teacher':teacher,
            'check_in':Student_Attendance.objects.filter(check_in__date=now().date()).count(),
            'check_out':Student_Attendance.objects.filter(check_out__date=now().date()).count(),
            'class':classes
        }
        return render(request, 'attendance.html', context)
    else:
        return redirect('school_mobile')
    
    

def video_feed_check_in(request):
    if request.method == 'POST' and request.FILES.get('frame'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
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
                    Student_Attendance.objects.create(
                        student_id=student['id'],
                        check_in=datetime.now(),
                        check_in_by_teacher=teacher,
                        )
                    send_push(student['tocken'], datetime.now() , f'{student["name"]} has checked in')
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

def send_push(tocken, title, body):
    if tocken and title and body:
        message = messaging.Message(
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title=str(title),
                    body=body,
                ),
            ),
            token=tocken
        )
        messaging.send(message)

def student_check_in(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
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
                        'tocken': s.student.tocken or '',
                    })
            except Exception as e:
                print(f"Error loading image for {s.student.name}: {e}")
                continue
        students_json = json.dumps(student_data)
        
        
        context={
            'teacher':teacher,
            'records':Student_Attendance.objects.filter(check_in__date=now().date()),
            'students_json':students_json
            
        }
        return render(request, 'student_check_in.html', context)
    else:
        return redirect('school_mobile')
 # Check in End
    
 # Check Out
 

def generate_frames_check_out(request):
    mobile = request.session['teacher_mobile']
    teacher = Teacher.objects.filter(mobile=mobile).first()
    
    video = cv2.VideoCapture(0)
    tolerance = 0.45
    marked_ids = set()

    # Load all student encodings and images
    student_data = []
    for s in Student_Image.objects.all():
        try:
            image = face_recognition.load_image_file(s.image.path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                original_image = cv2.imread(s.image.path)
                student_data.append({
                    'id': s.student.id,
                    'name': s.student.name,
                    'encoding': encodings[0],
                    'image': original_image
                })
        except:
            continue

    # For showing last matched student
    last_matched_image = None
    last_matched_name = ""
    today = now().date()

    while True:
        success, frame = video.read()
        if not success:
            break

        # Resize for faster processing
        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        # Detect faces and encodings
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for face_encoding, location in zip(encodings, locations):
            distances = [face_recognition.face_distance([s['encoding']], face_encoding)[0] for s in student_data]
            if distances and min(distances) <= tolerance:
                idx = np.argmin(distances)
                student = student_data[idx]

                # Check if attendance is already marked today
                already_marked = Student_Attendance.objects.filter(
                    student_id=student['id'],
                    check_out__date=today
                ).exists()

                label = f"{student['name']} (Already)" if already_marked else student['name']
                color = (0, 255, 0)
                
                student_in = Student_Attendance.objects.filter(
                    student_id=student['id'],
                    check_in__date=today
                ).exists()
                
                if not student_in:
                    label = f'{student["name"]} not in'
                    color = (255, 0, 0)
                else:
                    # Update thumbnail + name
                    last_matched_image = cv2.resize(student['image'], (100, 100))
                    last_matched_name = student['name']
                    
                    if not already_marked:
                        Student_Attendance.objects.filter(student_id=student['id'], check_in__date=today).update(check_out=now(), check_out_by_teacher=teacher )
                        marked_ids.add(student['id'])

            else:
                label = "Unknown"
                color = (0, 0, 255)

            # Draw face box
            top, right, bottom, left = [v * 4 for v in location]
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Show matched student image and name
        if last_matched_image is not None:
            frame[10:110, 10:110] = last_matched_image
            cv2.putText(frame, last_matched_name, (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Encode and yield frame
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    video.release()



def video_feed_check_out(request):
    if request.method == 'POST' and request.FILES.get('frame'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
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

                name = student['name']
                # Mark attendance if not already marked
                already_marked = Student_Attendance.objects.filter(
                    student_id=student['id'],
                    check_out__date=today
                ).exists()
                
                if already_marked:
                    name = f'{student["name"]} already checked out'
                
                student_in = Student_Attendance.objects.filter(
                    student_id=student['id'],
                    check_in__date=today
                ).exists()
                
                if not student_in:
                    name = f'{student["name"]} not in'
                
                if not already_marked and student_in:
                    Student_Attendance.objects.filter(student_id=student['id'], check_in__date=today).update(
                        check_out=datetime.now(), check_out_by_teacher=teacher )
                    send_push(student['tocken'], datetime.now() , f'{student["name"]} has checked in')
                # Return image from disk (reload for safety)
                try:
                    student_image_obj = Student_Image.objects.get(student_id=student['id'])
                    image = cv2.imread(student_image_obj.image.path)
                    image = cv2.resize(image, (150, 150))
                    _, buffer = cv2.imencode('.jpg', image)
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    return JsonResponse({
                        'status': 'matched',
                        'name': name,
                        'image': img_base64
                    })
                except:
                    return JsonResponse({'status': 'matched', 'name': name, 'image': None})

        return JsonResponse({'status': 'no match'})  # Unknown
    return JsonResponse({'error': 'Invalid request'}, status=400)
 
def student_check_out(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
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
                        'tocken': s.student.tocken or '',
                    })
            except Exception as e:
                print(f"Error loading image for {s.student.name}: {e}")
                continue
        students_json = json.dumps(student_data)
        
        
        context={
            'teacher':teacher,
            'records':Student_Attendance.objects.filter(check_in__date=now().date()),
            'students_json':students_json
            
        }
        return render(request, 'student_check_out.html', context)
    else:
        return redirect('school_mobile')
    
def teacher_notice(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        
        
        
        context={
            'teacher':teacher,
            
        }
        return render(request, 'teacher_notice.html', context)
    else:
        return redirect('school_mobile')
    
def teacher_received_notice(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        n = []
        for i in Notice.objects.filter().order_by('-id'):
            if i.to_teacher == teacher or i.to_all_teachers == 1 or i.to_school == 1 or i.to_class != None:
                n.append({
                    'id':i.id,
                    'notice_number':i.notice_number,
                    'by_clerk':i.by_clerk,
                    'by_teacher':i.by_teacher,
                    'by_admin':i.by_admin,
                    'batch':i.batch,
                    'to_class':i.to_class,
                    'to_student':i.to_student,
                    'to_school':i.to_school,
                    'to_teacher':i.to_teacher,
                    'title':i.title,
                    'description':i.description,
                    'added_date':i.added_date,
                    'readed_date':Readed_Notice.objects.filter(notice_id=i.id, read_by_teacher=teacher).first(),
                })
        
        context={ 
            'teacher':teacher,
            'all_notices':n,
        }
        return render(request, 'teacher_received_notice.html', context)
    else:
        return redirect('school_mobile')
 # Check Out End
    
def student_leaves(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        
        teacher_class = Class_teacher.objects.filter(teacher=teacher).first()
        
        leaves = []
        for l in Leave_letter.objects.filter(batch=teacher.batch).order_by('status'):
            sc = Class_student.objects.filter(student=l.student).first()
            if sc.school_class == teacher_class.school_class:
                leaves.append({
                    'id':l.id,
                    'student':l.student,
                    'from_date':l.from_date,
                    'to_date':l.to_date,
                    'added_date':l.added_date,
                    'status':l.status,
                    'accepted_date':l.accepted_date,
                    'reason':l.reason,
                    'gap_days':(l.to_date - l.from_date).days + 1
                })
        if 'approve' in request.POST:
            leave_id = request.POST.get('leave_id')
            leave = Leave_letter.objects.filter(id=leave_id).first()
            if leave.status == 0:
                leave.status = 1
                leave.accepted_date = now()
                leave.save()
                messages.success(request, f"Leave for {leave.student.name} has been approved.")
            else:
                messages.error(request, "Invalid leave request or already processed.")
            return redirect('/teacher/student_leaves/')
        if 'reject' in request.POST:
            leave_id = request.POST.get('leave_id')
            leave = Leave_letter.objects.filter(id=leave_id).first()
            if leave.status == 0:
                leave.status = 2
                leave.accepted_date = now()
                leave.save()
                messages.warning(request, f"Leave for {leave.student.name} has been rejected.")
            else:
                messages.error(request, "Invalid leave request or already processed.")
            return redirect('/teacher/student_leaves/')
        context={
            'teacher':teacher,
            'leaves':leaves
            
        }
        return render(request, 'student_leaves.html', context)
    else:
        return redirect('school_mobile')
    
def students_icard_for_teacher(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        teacher_class = Class_teacher.objects.filter(teacher=teacher).first()
        
        icard = []
        for s in Student.objects.filter(status=1):
            sc = Class_student.objects.filter(student=s).first()
            if sc:
                print(sc.school_class.name, teacher_class.school_class.name)
                if sc.school_class == teacher_class.school_class:
                    icard.append({
                        'id':s.id,
                        'name':s.name,
                        'address':s.address,
                        'mobile':s.mobile,
                        'date_of_birth':s.date_of_birth,
                        'class':sc.school_class.name,
                        'image':Student_Image.objects.filter(student=s).first(),
                    })
        
        
        context={
            'teacher':teacher,
            'icard':icard,
        }
        return render(request, 'students_icard_for_teacher.html', context)
    else:
        return redirect('school_mobile')
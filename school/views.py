from navbharat_school.includes import * 
# Create your views here.
def school_home(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        messages.success(request, 'Welcome to NAVBHARAT ENGLISH MEDIUM SCHOOL KARMALA!')
        context={
            'clerk':clerk
        }
        return render(request, 'school_home.html', context)
    else:
        return redirect('school_mobile')
    


@csrf_exempt
def student_image(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if 'add_image' in request.POST:
            id = request.POST.get('id')
            img_data = request.POST.get('img')  # base64 string

            format, imgstr = img_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{id}.{ext}')
            
            if Student_Image.objects.filter(student_id=id).exists():
                s = Student_Image.objects.filter(student_id=id).first()
                # Delete old image file from storage
                if s.image:
                    old_image_path = s.image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
            else:
                Student_Image.objects.create(student_id=id, added_by=clerk)
                
            s = Student_Image.objects.filter(student_id=id).first()
            s.image.save(f'{s.student.name}.webp', data, save=True)

            messages.success(request, 'Image Added Successfully')
        context={
            'clerk':clerk
        }
        return render(request, 'student/student_image.html', context)
    else:
        return redirect('school_mobile')
    
#teacher
def add_teacher(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        return_name = ''
        return_mobile = ''
        gender = ''
        aadhar_number = ''
        qualification = ''
        return_pin = ''
        if 'Add_Teacher' in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            aadhar_number = request.POST.get('aadhar_number')
            qualification = request.POST.get('qualification')

            # Basic validations
            if name == '':
                messages.error(request, 'Please enter teacher name!')
            elif mobile == '':
                messages.error(request, 'Please enter teacher mobile number!')
            elif pin == '':
                messages.error(request, 'Please enter teacher secret pin!')
            elif gender == '':
                messages.error(request, 'Please select teacher gender!')
            elif aadhar_number == '':
                messages.error(request, 'Please enter Aadhar number!')
            elif qualification == '':
                messages.error(request, 'Please enter qualification!')
            elif Teacher.objects.filter(mobile=mobile, batch=clerk.batch).exists():
                messages.error(request, 'This mobile number is already registered!')
            elif Teacher.objects.filter(aadhar_number=aadhar_number, batch=clerk.batch).exists():
                messages.error(request, 'This Aadhar number is already registered!')
            else:
                Teacher.objects.create(
                    batch=clerk.batch,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    gender=gender,
                    aadhar_number=aadhar_number,
                    qualification=qualification
                )
                messages.success(request, 'Teacher added successfully!')
                return redirect('add_teacher')
            return_name = name
            return_mobile = mobile
            return_pin = pin
        if 'edit_teacher' in request.POST:
            teacher_id = request.POST.get('teacher_id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            aadhar_number = request.POST.get('aadhar_number')
            qualification = request.POST.get('qualification')

            if name == '':
                messages.error(request, 'Please enter teacher name!')
            elif mobile == '':
                messages.error(request, 'Please enter teacher mobile number!')
            elif pin == '':
                messages.error(request, 'Please enter teacher secret pin!')
            elif gender == '':
                messages.error(request, 'Please select teacher gender!')
            elif aadhar_number == '':
                messages.error(request, 'Please enter Aadhar number!')
            elif qualification == '':
                messages.error(request, 'Please enter qualification!')
            elif Teacher.objects.filter(mobile=mobile, batch=clerk.batch).exclude(id=teacher_id).exists():
                messages.error(request, 'This mobile number is already registered!')
            elif Teacher.objects.filter(aadhar_number=aadhar_number, batch=clerk.batch).exclude(id=teacher_id).exists():
                messages.error(request, 'This Aadhar number is already registered!')
            else:
                Teacher.objects.filter(id=teacher_id).update(
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    gender=gender,
                    aadhar_number=aadhar_number,
                    qualification=qualification
                )
                messages.success(request, 'Teacher updated successfully!')
            return redirect('add_teacher')
        if 'active'in request.POST:
            teacher_id = request.POST.get('id')
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.status = 0
            teacher.save()
            return redirect('add_teacher')
        if 'deactive'in request.POST:
            teacher_id = request.POST.get('id')
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.status = 1
            teacher.save()
            return redirect('add_teacher')
        if 'Change_branding_status' in request.POST:
            teacher_id = request.POST.get('id')
            teacher = Teacher.objects.get(id=teacher_id)
            if teacher.branding_status == 1:
                teacher.branding_status = 0
            else:
                teacher.branding_status = 1
            teacher.save()
            return redirect('add_teacher')
        context={
            'clerk':clerk,
            'teachers': Teacher.objects.filter(batch=clerk.batch).order_by('-id'),
            'return_name': return_name,
            'return_mobile': return_mobile,
            'return_pin': return_pin,
            'return_gender': gender,
            'return_aadhar_number': aadhar_number,
            'return_qualification': qualification,
        }
        return render(request, 'teacher/add_teacher.html', context)
    else:
        return redirect('school_mobile')
    
#student
def add_student(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        
        return_name = ''
        return_mobile = ''
        return_aadhar_number = ''
        if 'Add_Student'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            aadhar_number = request.POST.get('aadhar_number')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            if name == '':
                messages.error(request, 'Please enter Student name!')

            elif mobile == '':
                messages.error(request, 'Please enter Parent mobile number!')

            elif aadhar_number == '':
                messages.error(request, 'Please enter Student Aadhar_number number!')
                
            elif gender == '':
                messages.error(request, 'Please Select Student gender!')
                

            elif Student.objects.filter(aadhar_number=aadhar_number).exists():
                messages.error(request, 'This Student is already registered!')
            else:
                Student(
                    name=name,
                    mobile=mobile,
                    aadhar_number=aadhar_number,
                    secret_pin=pin or str('0000'),
                    gender=gender,
                    added_by=clerk,
                ).save()
                messages.success(request, 'Student added successfully!')
                return redirect('add_student')
            return_name = name
            return_mobile = mobile
            return_aadhar_number = aadhar_number
        if 'edit_student' in request.POST:
            student_id = request.POST.get('student_id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            aadhar_number = request.POST.get('aadhar_number')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            if name == '':
                messages.error(request, 'Please enter Student name!')

            elif mobile == '':
                messages.error(request, 'Please enter Parent mobile number!')

            elif aadhar_number == '':
                messages.error(request, 'Please enter Student Aadhar_number number!')
                
            elif gender == '':
                messages.error(request, 'Please Select Student gender!')
                
            elif Student.objects.filter(aadhar_number=aadhar_number).exclude(id=student_id).exists():
                messages.error(request, 'This Student is already registered!')
            else:
                Student.objects.filter(id=student_id).update(
                    name=name,
                    mobile=mobile,
                    aadhar_number=aadhar_number,
                    secret_pin=pin,
                    gender=gender,
                )
                messages.success(request, 'Student updated successfully!')
                return redirect('add_student')
        if 'active'in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.status = 0
            student.save()
            return redirect('add_student')
        if 'deactive'in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.status = 1
            student.save()
            return redirect('add_student')
        context={
            'clerk':clerk,
            'students': Student.objects.filter().order_by('-id'),
            'return_name': return_name,
            'return_mobile': return_mobile,
            'return_aadhar_number': return_aadhar_number,
        }
        return render(request, 'student/add_student.html', context)
    else:
        return redirect('school_mobile')
    
#Class
def add_class(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()

        if 'Add_Class'in request.POST:
            name = request.POST.get('name').upper()

            if name == '':
                messages.error(request, 'Please enter class name!')
                
            elif School_class.objects.filter(name=name, batch=clerk.batch).exists():
                messages.error(request, 'This Class number is already registered!')
            else:
                School_class(
                    added_by=clerk,
                    batch=clerk.batch,
                    name=name
                ).save()
                messages.success(request, 'Clss added successfully!')
                return redirect('add_class')
        if 'edit_class' in request.POST:
            class_id = request.POST.get('class_id')
            name = request.POST.get('name')
            if name == '':
                messages.error(request, 'Please enter class name!')
            elif School_class.objects.filter(name=name, batch=clerk.batch).exclude(id=class_id).exists():
                messages.error(request, 'This mobile number is already registered!')
            else:
                School_class.objects.filter(id=class_id).update(name=name)
                messages.success(request, 'Class updated successfully!')
                return redirect('add_class')
        if 'active'in request.POST:
            Class_id = request.POST.get('id')
            c = School_class.objects.get(id=Class_id)
            c.status = 0
            c.save()
            return redirect('add_class')
        if 'deactive'in request.POST:
            Class_id = request.POST.get('id')
            c = School_class.objects.get(id=Class_id)
            c.status = 1
            c.save()
            return redirect('add_class')
        context={
            'clerk':clerk,
            'classes': School_class.objects.filter(batch=clerk.batch).order_by('-id'),
        }

        return render(request, 'class/add_class.html', context)
    else:
        return redirect('school_mobile')
    
def select_student_class(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()

        context={
            'clerk':clerk,
            'classes': School_class.objects.filter(batch=clerk.batch).order_by('-id'),
        }

        return render(request, 'class/select_student_class.html', context)
    else:
        return redirect('school_mobile')
    
@csrf_exempt
def select_student_class_id(request, id):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if 'remove_selected_student'in request.POST:
            tid = request.POST.get('id')
            c = Class_student.objects.filter(id=tid).first()
            messages.success(request, f'Removed Student {c.student.name}')
            c.delete()
            return redirect(f'/school/select_student_class/{id}/')
        context={
            'clerk':clerk,
            'selected_students':Class_student.objects.filter(school_class_id=id).order_by('id'),
            'class':School_class.objects.filter(id=id).first()
        }

        return render(request, 'class/select_student_class_id.html', context)
    else:
        return redirect('school_mobile')
    
@csrf_exempt
def select_class_teacher(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        classes = []
        selected_teacher_id = []
        for c in  School_class.objects.filter(added_by__batch=clerk.batch).order_by('-id'):
            cl = Class_teacher.objects.filter(school_class_id=c.id).first() or ''
            if cl:
                selected_teacher_id.append(cl.teacher_id)
            classes.append({
                'id':c.id,
                'name':c.name,
                'class_teacher':cl,
            })
        if 'select_class_teacher'in request.POST:
            class_id = request.POST.get('class_id')
            teacher_id = request.POST.get('teacher_id')
            cl = Class_teacher.objects.filter(school_class_id=class_id).first()
            if cl:
                cl.teacher_id = teacher_id
                cl.save
            else:
                Class_teacher(
                    added_by=clerk,
                    school_class_id=class_id,
                    teacher_id=teacher_id
                ).save()
            messages.success(request, 'Class teacher assigned successfully!')
            return redirect('select_class_teacher')
        if 'remove_class_teacher'in request.POST:
            id = request.POST.get('id')
            Class_teacher.objects.filter(school_class_id=id).delete()
            messages.success(request, 'Class teacher removed successfully!')
            return redirect('select_class_teacher')
        context={
            'clerk':clerk,
            'classes':classes,
            'teachers':Teacher.objects.filter(batch=clerk.batch).exclude(id__in=selected_teacher_id)
            
        }

        return render(request, 'class/select_class_teacher.html', context)
    else:
        return redirect('school_mobile')
    
def add_subject(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()

        if 'Add_Subject' in request.POST:
            name = request.POST.get('name').upper()

            if name == '':
                messages.error(request, 'Please enter subject name!')
            elif Subject.objects.filter(name=name, added_by__batch=clerk.batch).exists():
                messages.error(request, 'This subject is already registered!')
            else:
                Subject(
                    added_by=clerk,
                    name=name
                ).save()
                messages.success(request, 'Subject added successfully!')
                return redirect('add_subject')
        if 'edit_subject' in request.POST:
            subject_id = request.POST.get('subject_id')
            name = request.POST.get('name').upper()
            if name == '':
                messages.error(request, 'Please enter subject name!')
            elif Subject.objects.filter(name=name, added_by__batch=clerk.batch).exclude(id=subject_id).exists():
                messages.error(request, 'This subject is already registered!')
            else:
                Subject.objects.filter(id=subject_id).update(name=name)
                messages.success(request, 'Subject updated successfully!')
                return redirect('add_subject')
        if 'active' in request.POST:
            subject_id = request.POST.get('id')
            subject = Subject.objects.get(id=subject_id)
            subject.status = 0
            subject.save()
            return redirect('add_subject')
        if 'deactive' in request.POST:
            subject_id = request.POST.get('id')
            subject = Subject.objects.get(id=subject_id)
            subject.status = 1
            subject.save()
            return redirect('add_subject')
        context = {
            'clerk': clerk,
            'subjects': Subject.objects.filter(added_by__batch=clerk.batch).order_by('-id'),
        }

        return render(request, 'subject/add_subject.html', context)
    else:
        return redirect('school_mobile')
    
@csrf_exempt
def select_subject_class_and_teacher(request):
    if not request.session.get('school_mobile'):
        return redirect('school_login')

    mobile = request.session['school_mobile']
    clerk = Clerk.objects.filter(mobile=mobile).first()

    if not clerk:
        messages.error(request, "Clerk not found.")
        return redirect('login')

    if 'select'in request.POST:
        subject_id = request.POST.get('subject_id')
        class_id = request.POST.get('class_id')
        teacher_id = request.POST.get('teacher_id')

        # Check for duplicates
        already_exists = Subject_class_and_teacher.objects.filter(
            subject_id=subject_id,
            school_class_id=class_id,
            teacher_id=teacher_id
        ).exists()

        if already_exists:
            messages.error(request, 'This subject-class-teacher combination is already selected.')
        else:
            Subject_class_and_teacher.objects.create(
                added_by=clerk,
                subject_id=subject_id,
                school_class_id=class_id,
                teacher_id=teacher_id
            )
            messages.success(request, 'Combination added successfully.')

        return redirect('select_subject_class_and_teacher')
    if 'remove'in request.POST:
        id = request.POST.get('id')
        Subject_class_and_teacher.objects.filter(id=id).delete()
        messages.success(request, 'Combination removed successfully.')
        return redirect('select_subject_class_and_teacher')
        
    # GET request
    batch = clerk.batch
    context = {
        'clerk': clerk,
        'classes': School_class.objects.filter(added_by__batch=batch).order_by('-id'),
        'subjects': Subject.objects.filter(added_by__batch=batch).order_by('-id'),
        'teachers': Teacher.objects.filter(batch=batch).order_by('-id'),
        'selected_subject_class_teacher': Subject_class_and_teacher.objects.filter(added_by__batch=batch)
    }

    return render(request, 'subject/select_subject_class_and_teacher.html', context)
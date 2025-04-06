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
        return redirect('login')
    
def add_teacher(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        return_name = ''
        return_mobile = ''
        return_pin = ''
        if 'Add_Teacher'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            if name == '':
                messages.error(request, 'Please enter teacher name!')

            elif mobile == '':
                messages.error(request, 'Please enter teacher mobile number!')

            elif pin == '':
                messages.error(request, 'Please enter teacher secret pin!')

            elif Teacher.objects.filter(mobile=mobile, batch=clerk.batch).exists():
                messages.error(request, 'This mobile number is already registered!')
            else:
                Teacher(
                    batch=clerk.batch,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
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
            if name == '':
                messages.error(request, 'Please enter teacher name!')
            elif mobile == '':
                messages.error(request, 'Please enter teacher mobile number!')
            elif pin == '':
                messages.error(request, 'Please enter teacher secret pin!')
            elif Teacher.objects.filter(mobile=mobile, batch=clerk.batch).exclude(id=teacher_id).exists():
                messages.error(request, 'This mobile number is already registered!')
            else:
                Teacher.objects.filter(id=teacher_id).update(name=name, mobile=mobile, pin=pin)
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
        context={
            'clerk':clerk,
            'teachers': Teacher.objects.filter(batch=clerk.batch).order_by('-id'),
            'return_name': return_name,
            'return_mobile': return_mobile,
            'return_pin': return_pin,
        }
        return render(request, 'add_teacher.html', context)
    else:
        return redirect('login')
    
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
        return render(request, 'add_student.html', context)
    else:
        return redirect('login')
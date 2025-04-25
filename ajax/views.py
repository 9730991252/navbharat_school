
from navbharat_school.includes import *

def search_student(request):
    if request.method == 'GET':
        words = request.GET['words']
        batch_id = request.GET['batch_id']
        student = []
        for s in Student.objects.filter(name__icontains=words):
            selected_status = 0
            c = Class_student.objects.filter(student=s, batch_id=batch_id).first()
            class_name = ''
            if c:
                class_name = c.school_class.name
                selected_status = 1
            print(class_name)
            student.append({
                'id':s.id,
                'name':s.name,
                'mobile':s.mobile,
                'aadhar_number':s.aadhar_number,
                'secret_pin':s.secret_pin,
                'gender':s.gender,
                'selected_status':selected_status,
                'selected_class':class_name
            })
        context = {
            'student':student[:10]
        }
        t = render_to_string('search_student.html', context)
    return JsonResponse({'t': t})
 
def search_student_image(request):
    if request.method == 'GET':
        words = request.GET['words']
        batch_id = request.GET['batch_id']
        student = []
        for s in Student.objects.filter(name__icontains=words):
            student.append({
                'id':s.id,
                'name':s.name,
                'mobile':s.mobile,
                'aadhar_number':s.aadhar_number,
                'secret_pin':s.secret_pin,
                'gender':s.gender,
                'img':Student_Image.objects.filter(student=s).first(),
            })
        context = {
            'student':student[:10]
        }
        t = render_to_string('search_student_image.html', context)
    return JsonResponse({'t': t})

def search_student_for_edit(request):
    if request.method == 'GET':
        words = request.GET['words']
        context = {
            'students':Student.objects.filter(name__icontains=words)
        }
        t = render_to_string('search_student_for_edit.html', context)
    return JsonResponse({'t': t})

def search_student_for_check_in(request):
    if request.method == 'GET':
        words = request.GET['words']
        batch_id = request.GET['batch_id']
        student = []
        for s in Student.objects.filter(name__icontains=words):
            if not Student_Attendance.objects.filter(student=s, check_in__date=date.today()).exists():
                student.append({
                    'id':s.id,
                    'name':s.name,
                    'mobile':s.mobile,
                    'aadhar_number':s.aadhar_number,
                    'secret_pin':s.secret_pin,
                    'gender':s.gender,
                    'img':Student_Image.objects.filter(student=s).first(),
                })
        context = {
            'student':student[:10]
        }
        t = render_to_string('search_student_for_check_in.html', context)
    return JsonResponse({'t': t})

def search_student_for_check_out(request):
    if request.method == 'GET':
        words = request.GET['words']
        student = []
        for s in Student.objects.filter(name__icontains=words):
            a = Student_Attendance.objects.filter(student_id=s.id, check_in__date=date.today()).first()
            if a:
                if a.check_out == None:
                    student.append({
                        'id':s.id,
                        'name':s.name,
                        'mobile':s.mobile,
                        'aadhar_number':s.aadhar_number,
                        'secret_pin':s.secret_pin,
                        'gender':s.gender,
                        'img':Student_Image.objects.filter(student=s).first(),
                    })
        context = {
            'student':student[:10]
        }
        t = render_to_string('search_student_for_check_out.html', context)
    return JsonResponse({'t': t})
 

def select_student(request):
    if request.method == 'GET':
        id = request.GET['id']
        batch_id = request.GET['batch_id']
        class_id = request.GET['class_id']
        clerk_id = request.GET['clerk_id']
        Class_student(
            added_by_id = clerk_id,
            batch_id = batch_id,
            school_class_id = class_id,
            student_id = id
        ).save()
        context = {
            'selected_students':Class_student.objects.filter(school_class_id=class_id).order_by('id')
        }
        t = render_to_string('select_student.html', context)
    return JsonResponse({'t': t})
def check_in_student_manual(request):
    if request.method == 'GET':
        id = request.GET['s_id']
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        Student_Attendance(
            student_id=id,
            check_in_by_teacher=teacher,
            check_in=datetime.now(),
            check_in_type=0
        ).save()
    return JsonResponse({'t': 't'})
def check_out_student_manual(request):
    if request.method == 'GET':
        id = request.GET['s_id']
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        
        Student_Attendance.objects.filter(student_id=id, check_in__date=date.today()).update(
            check_out = now(),
            check_out_by_teacher=teacher
        )

    return JsonResponse({'t': 't'})

def search_attrndance_day(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))

        # Filter by year and month from check_in field
        day = Student_Attendance.objects.filter(
            student_id=student_id,
            check_in__year=year,
            check_in__month=month
        ).values()

        attrndance_day = list(day)
        
        
        return JsonResponse({'attrndance_day': attrndance_day})
def search_holiday(request):
    if request.method == 'GET':
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))

        # Filter by year and month from check_in field
        day = Holidays.objects.filter(
            date__year=year,
            date__month=month
        ).values()

        holiday = list(day)
        
        
        return JsonResponse({'holiday': holiday})

def check_day(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))
        day = int(request.GET.get('day'))
        print(student_id, year, month, day)

        # Filter by year and month from check_in field
        attendance = Student_Attendance.objects.filter(
            student_id=student_id,
            check_in__year=year,
            check_in__month=month,
            check_in__day=day
        ).first()

        holiday = Holidays.objects.filter(
            date__year=year,
            date__month=month,
            date__day=day
        )
        
        t = render_to_string('check_day.html', {
            'attendance': attendance,
            'date': date(year, month, day),
            'holiday': holiday,
            })
        return JsonResponse({'t': t})
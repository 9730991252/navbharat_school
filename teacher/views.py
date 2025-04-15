from navbharat_school.includes import *

# Create your views here.
def teacher_home(request):
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
        context={
            'teacher':teacher,
        }
        return render(request, 'attendance.html', context)
    else:
        return redirect('school_mobile')
def student_check_in(request):
    if request.session.has_key('teacher_mobile'):
        mobile = request.session['teacher_mobile']
        teacher = Teacher.objects.filter(mobile=mobile).first()
        context={
            'teacher':teacher,
        }
        return render(request, 'attendance.html', context)
    else:
        return redirect('school_mobile')
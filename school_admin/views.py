from navbharat_school.includes import * 

# Create your views here.
def admin_home(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        context={
            'total_students':Student.objects.all().count(),
            'male_students':Student.objects.filter(gender='MALE').count(),
            'female_students':Student.objects.filter(gender='FEMALE').count(),
            'total_teacher':Teacher.objects.all().count(),
            'male_teacher':Teacher.objects.filter(gender='MALE').count(),
            'female_teacher':Teacher.objects.filter(gender='FEMALE').count(),
        }
        return render(request, 'admin_home.html', context)
    else:
        return redirect('admin_login')
    
def admin_view_students(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        s = []
        for i in Student.objects.all():
            s.append({
                'id':i.id,
                'name':i.name,
                'mobile':i.mobile,
                'aadhar_number':i.aadhar_number,
                'gender':i.gender,
                'img':Student_Image.objects.filter(student_id=i.id).first(),
                'class':Class_student.objects.filter(student_id=i.id).first(),
            })
        context={
            'students':s,
            'total_students':Student.objects.all().count(),
            'male_students':Student.objects.filter(gender='MALE').count(),
            'female_students':Student.objects.filter(gender='FEMALE').count(),
        }
        return render(request, 'admin_view_students.html', context)
    else:
        return redirect('admin_login')
    
def admin_view_teacher(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        s = []
        for i in Teacher.objects.all():
            s.append({
                'id':i.id,
                'name':i.name,
                'mobile':i.mobile,
            })
        context={
            'teachers':s,
        }
        return render(request, 'admin_view_teacher.html', context)
    else:
        return redirect('admin_login')
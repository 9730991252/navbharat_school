from navbharat_school.includes import * 

# Create your views here.
def admin_home(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_login.objects.filter(mobile=mobile).first()
        classes = []
        for c in School_class.objects.filter(batch=a.batch, status=1):
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
            'total_students':Student.objects.all().count(),
            'male_students':Student.objects.filter(gender='MALE').count(),
            'female_students':Student.objects.filter(gender='FEMALE').count(),
            'total_teacher':Teacher.objects.all().count(),
            'male_teacher':Teacher.objects.filter(gender='MALE').count(),
            'female_teacher':Teacher.objects.filter(gender='FEMALE').count(),
            'check_in':Student_Attendance.objects.filter(check_in__date=now().date()).count(),
            'check_out':Student_Attendance.objects.filter(check_out__date=now().date()).count(),
            'class':classes
        }
        return render(request, 'admin_home.html', context)
    else:
        return redirect('admin_login')
def todayes_attendence(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        a = Admin_login.objects.filter(mobile=mobile).first()
        classes = []
        for c in School_class.objects.filter(batch=a.batch, status=1):
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
            'total_students':Student.objects.all().count(),
            'male_students':Student.objects.filter(gender='MALE').count(),
            'female_students':Student.objects.filter(gender='FEMALE').count(),
            'total_teacher':Teacher.objects.all().count(),
            'male_teacher':Teacher.objects.filter(gender='MALE').count(),
            'female_teacher':Teacher.objects.filter(gender='FEMALE').count(),
            'check_in':Student_Attendance.objects.filter(check_in__date=now().date()).count(),
            'check_out':Student_Attendance.objects.filter(check_out__date=now().date()).count(),
            'class':classes
        }
        return render(request, 'todayes_attendence.html', context)
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
    
def admin_notice(request):
    if request.session.has_key('admin_mobile'):
        mobile = request.session['admin_mobile']
        context={
        }
        return render(request, 'admin_notice.html', context)
    else:
        return redirect('admin_login')
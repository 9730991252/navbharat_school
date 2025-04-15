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
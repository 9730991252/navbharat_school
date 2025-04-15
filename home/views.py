from navbharat_school.includes import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def school_login(request):
    if request.method == "POST":
        batch_id=request.POST ['batch_id']
        number=request.POST ['mobile']
        pin=request.POST ['pin']
        c= Clerk.objects.filter(batch_id=batch_id,mobile=number,secret_pin=pin,status=1)
        if c:
            request.session['school_mobile'] = request.POST["mobile"]
            return redirect('school_home')
        else:
            messages.error(request,f"Mobile Number or Secret Pin invalid.")
            return redirect('/school_login/')
    context = {
        'batch':Batch.objects.all(),
    }
    return render(request, 'school_login.html', context)

def admin_login(request):
    if request.session.has_key('admin_mobile'):
         return redirect('admin_home')
    if request.method == "POST":
        batch_id=request.POST ['batch_id']
        number=request.POST ['mobile']
        pin=request.POST ['pin']
        a = Admin_login.objects.filter(mobile=number, pin=pin).first()
        if a:
            a.batch_id=batch_id
            request.session['admin_mobile'] = request.POST["mobile"]
            return redirect('admin_home')
        else:
            messages.error(request,f"Mobile Number or Secret Pin invalid.")
            return redirect('/admin_login/')
    context = {
        'batch':Batch.objects.all(),
    }
    return render(request, 'admin_login.html',context)

def parent_login(request):
    batch = Batch.objects.filter(status=1, start_date__lte=date.today()).first()  
    if request.session.has_key('parent_mobile'):
         return redirect('student_home', batch.id)
    if request.method == "POST":
        number=request.POST ['mobile']
        pin=request.POST ['pin']
        s= Student.objects.filter(mobile=number,secret_pin=pin,status=1)
        if s:
            request.session['parent_mobile'] = request.POST["mobile"]
            return redirect('student_home', batch.id)
        else:
            messages.error(request,f"Mobile Number or Secret Pin invalid.")
            return redirect('/school_login/')
    return render(request, 'parent_login.html')

def teacher_login(request):
    if request.method == "POST":
        batch_id=request.POST ['batch_id']
        number=request.POST ['mobile']
        pin=request.POST ['pin']
        c= Teacher.objects.filter(batch_id=batch_id,mobile=number,pin=pin,status=1)
        if c:
            request.session['teacher_mobile'] = request.POST["mobile"]
            return redirect('teacher_home')
        else:
            messages.error(request,f"Mobile Number or Secret Pin invalid.")
            return redirect('/teacher_login/')
    context = {
        'batch':Batch.objects.all(),
    }
    return render(request, 'teacher_login.html',context)
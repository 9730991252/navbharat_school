from django.shortcuts import render, redirect, get_object_or_404
from home.models import *
from sunil.models import *
from teacher.models import *
from school.models import *
from school_admin.models import *
from student.models import *
from django.contrib import messages
from datetime import date
from django.db.models import *
from django.db.models import Avg, Sum, Min, Max
from django.db.models import F
# Create your views here.
def check_new_visitor(request):
    v = 1
    if request.session.has_key('admin_mobile'):
        v = 0
    if request.session.has_key('school_mobile'):
        v = 0
    if request.session.has_key('parent_mobile'):
        v = 0
    if request.session.has_key('teacher_mobile'):
        v = 0
    if not web_visitor.objects.all().first():
        web_visitor.objects.create(
            count=v
        )
    else:
        web_visitor.objects.all().update(
            count=F('count') + v
        )
    return web_visitor.objects.all().first().count

def check_avalable_cash(request, batch):
    avalable_cash = Student_received_Fee_Cash.objects.filter(added_by__batch=batch).aggregate(Sum('received_amount'))['received_amount__sum']
    avalable_cash -= Cash_Transfer_To_Bank.objects.filter(batch=batch).aggregate(Sum('amount'))['amount__sum'] or 0
    avalable_cash -= Cash_Transfer_To_Admin.objects.filter(batch=batch).aggregate(Sum('amount'))['amount__sum'] or 0
    avalable_cash -= Expenses.objects.filter(batch=batch, type='cash').aggregate(Sum('amount'))['amount__sum'] or 0
    return avalable_cash


def index(request):
    context = {
        'visitor': check_new_visitor(request),
        'teachers_count': Teacher.objects.filter(status=1, branding_status=1).count(),
        'teachers': Teacher.objects.filter(status=1, branding_status=1),
    }
    return render(request, 'index.html', context)

def logout(request):
    if request.session.has_key('admin_mobile'):
        del request.session['admin_mobile']
        
    if request.session.has_key('school_mobile'):
        del request.session['school_mobile']
        
    if request.session.has_key('parent_mobile'):
        del request.session['parent_mobile']
        
    if request.session.has_key('teacher_mobile'):
        del request.session['teacher_mobile']
        
    return redirect('/')
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
        'visitor': check_new_visitor(request),
        
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
            a.save()
            request.session['admin_mobile'] = request.POST["mobile"]
            return redirect('admin_home')
        else:
            messages.error(request,f"Mobile Number or Secret Pin invalid.")
            return redirect('/admin_login/')
    context = {
        'batch':Batch.objects.all(),
        'visitor': check_new_visitor(request),
        
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
            return redirect('/parent_login/')
    context={
        'visitor': check_new_visitor(request),
        
    }
    return render(request, 'parent_login.html', context)

def teacher_login(request):
    if request.session.has_key('teacher_mobile'):
        print('yes')
        return redirect('teacher_home')
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
        'visitor': check_new_visitor(request),
        
    }
    return render(request, 'teacher_login.html',context)
from navbharat_school.includes import *
# Create your views here.
def student_home(request, batch_id):
    if request.session.has_key('parent_mobile'):
        mobile = request.session['parent_mobile']
        student = Student.objects.filter(mobile=mobile).first()
        current_batch = Batch.objects.get(id=batch_id)
        
        context={
            'student':student,
            'batches':Batch.objects.filter(status=1),
            'current_batch':Batch.objects.get(id=batch_id),
        }
        return render(request, 'student_home.html', context)
    else:
        return redirect('login')
    
def notice(request, batch_id):
    if request.session.has_key('parent_mobile'):
        mobile = request.session['parent_mobile']
        student = Student.objects.filter(mobile=mobile).first()
        current_batch = Batch.objects.get(id=batch_id)
        
        context={
            'student':student,
            'batches':Batch.objects.filter(status=1),
            'current_batch':Batch.objects.get(id=batch_id),
        }
        return render(request, 'notice.html', context)
    else:
        return redirect('login')
    
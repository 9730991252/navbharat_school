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
    
def videos(request, batch_id):
    if request.session.has_key('parent_mobile'):
        mobile = request.session['parent_mobile']
        student = Student.objects.filter(mobile=mobile).first()
        current_batch = Batch.objects.get(id=batch_id)
        
        context={
            'student':student,
            'student_image':Student_Image.objects.filter(student_id=student.id),
            'batches':Batch.objects.filter(status=1),
            'current_batch':Batch.objects.get(id=batch_id),
        }
        return render(request, 'videos.html', context)
    else:
        return redirect('login')
    
from django.contrib import messages

def student_profile(request, batch_id):
    if request.session.has_key('parent_mobile'):
        mobile = request.session['parent_mobile']
        student = Student.objects.filter(mobile=mobile).first()
        current_batch = Batch.objects.get(id=batch_id)

        if request.method == 'POST':
            new_pin = request.POST.get('new_pin')
            if new_pin and new_pin.isdigit() and len(new_pin) == 4:
                student.secret_pin = new_pin
                student.save()
                messages.success(request, 'PIN changed successfully.')
            else:
                messages.error(request, 'Please enter a valid 4-digit PIN.')

        context = {
            'student': student,
            'student_image': Student_Image.objects.filter(student_id=student.id),
            'batches': Batch.objects.filter(status=1),
            'current_batch': current_batch,
        }
        return render(request, 'student_profile.html', context)
    else:
        return redirect('login')
    
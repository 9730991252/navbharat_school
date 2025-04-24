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
            'class':Class_student.objects.filter(student=student, batch=current_batch).first(),
            'attendance':Student_Attendance.objects.filter(student=student, check_in__date=date.today()).first(),
            'student_image':Student_Image.objects.filter(student_id=student.id).first(),
        }
        return render(request, 'student_home.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def save_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'status': 'error', 'message': 'No token provided'}, status=400)
            else:
                mobile = request.session['parent_mobile']
                student = Student.objects.filter(mobile=mobile).first()
                student.tocken = token
                student.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    
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
    
@csrf_exempt
def leave_letter(request, batch_id):
    if request.session.has_key('parent_mobile'):
        mobile = request.session['parent_mobile']
        student = Student.objects.filter(mobile=mobile).first()
        current_batch = Batch.objects.get(id=batch_id)
        if 'send_leave_letter'in request.POST:
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            reason = request.POST.get('reason')
            Leave_letter.objects.create(batch=current_batch,
                                        student=student,
                                        from_date=from_date,
                                        to_date=to_date,
                                        reason=reason
                                        )
            messages.success(request, 'Leave letter sent successfully.')
            return redirect('leave_letter', batch_id=batch_id)
        elif 'edit_leave_letter' in request.POST:
            leave_id = request.POST.get('leave_id')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            reason = request.POST.get('reason')
            leave_letter = Leave_letter.objects.get(id=leave_id, student=student)
            leave_letter.from_date = from_date
            leave_letter.to_date = to_date
            leave_letter.reason = reason
            leave_letter.save()
            messages.success(request, 'Leave letter updated successfully.')
            return redirect('leave_letter', batch_id=batch_id)
        context={
            'student':student,
            'batches':Batch.objects.filter(status=1),
            'current_batch':Batch.objects.get(id=batch_id),
            'leave_letter':Leave_letter.objects.filter(student=student).order_by('-id'),
        }
        return render(request, 'leave_letter.html', context)
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
    
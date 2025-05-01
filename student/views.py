from navbharat_school.includes import *
# Create your views here.

def save_student_used_count(s_id):
    obj, created = Student_used_count.objects.get_or_create(student_id=s_id, defaults={'used_count': 1})
    if not created:
        obj.used_count = F('used_count') + 1
        obj.save()
        
def student_home(request, batch_id):
    if request.session.has_key('parent_mobile'):
        mobile = request.session['parent_mobile']
        student = Student.objects.filter(mobile=mobile).first()
        current_batch = Batch.objects.get(id=batch_id)
        save_student_used_count(student.id)
        
        
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
    if not request.session.get('parent_mobile'):
        return redirect('login')
    
    mobile = request.session['parent_mobile']
    student = Student.objects.filter(mobile=mobile).first()
    student_class = Class_student.objects.filter(student=student).first()
    if not student:
        return redirect('login')
    
    student_class = Class_student.objects.filter(student=student).first()
    print(student_class.school_class.id)
    current_batch = get_object_or_404(Batch, id=batch_id)

    notices = Notice.objects.filter(batch=current_batch, status=1).order_by('-id')

    # Filter notices based on student
    filtered_notices = [
    notice for notice in notices if (
        (notice.to_student == student) or
        (notice.to_school == 1) or
        (notice.to_class == student_class.school_class) or
        (notice.to_teacher == '')
    )
    ]

    # Get list of read notices and read dates
    readed_notices = Readed_Notice.objects.filter(
        read_by_student=student,
        notice__in=filtered_notices
    )
    
    readed_notice_dict = {rn.notice_id: rn.readed_date for rn in readed_notices}
    read_notice_ids = list(readed_notice_dict.keys())

    # Attach readed_date to each notice
    all_notices = []
    for notice in filtered_notices:
        notice.readed_date = readed_notice_dict.get(notice.id)
        all_notices.append(notice)

    context = {
        'student': student,
        'batches': Batch.objects.filter(status=1),
        'current_batch': current_batch,
        'all_notices': all_notices,
        'read_notice_ids': read_notice_ids,
    }
    return render(request, 'notice.html', context)
    
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
    
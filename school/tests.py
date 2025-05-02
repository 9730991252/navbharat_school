@csrf_exempt  # Only for testing; remove in production
def student_fee_detail(request, id):
    if request.session.get('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        student = get_object_or_404(Student, id=id)
        student_img = Student_Image.objects.filter(student=student).first()
        class_info = Class_student.objects.filter(student=student, batch=clerk.batch).select_related('batch', 'school_class').first()
        total_fee = Student_Total_Fee.objects.filter(student=student, added_by__batch=clerk.batch).first()
        remaning_fee = total_fee.total_fee or 0
        cash_fee = Student_received_Fee_Cash.objects.filter(student=student, added_by__batch=clerk.batch)
        paid_fee = int(cash_fee.aggregate(Sum('received_amount'))['received_amount__sum'])
        remaning_fee -= paid_fee
        if 'save_total_fee' in request.POST:
            total_amount = request.POST.get('total_amount')
            discount_amount = request.POST.get('discount_amount')
            # Save fee to database (if model exists)
            Student_Total_Fee.objects.create(
                student=student,
                added_by=clerk,
                total_fee=total_amount,
                discount=discount_amount
            )
            messages.success(request, 'Fee Genereated successfully')
            return redirect('student_fee_detail', id=id)

        # Save cash fee logic
        if 'save_cash_fee' in request.POST:
            cash_amount = request.POST.get('received_amount')
            pdate = request.POST.get('date')
            # Save cash fee to database (if model exists)
            Student_received_Fee_Cash.objects.create(
                student=student,
                added_by=clerk,
                received_amount=cash_amount,
                paid_date=pdate,
            )
            messages.success(request, 'Cash Fee Saved successfully')
            return redirect('student_fee_detail', id=id)

        context = {
            'clerk': clerk,
            'student': student,
            'student_img': student_img,
            'class_info': class_info,
            'total_fee': total_fee,
            'todayes_date':date.today(),
            'cash_fee':cash_fee,
            'remaning_fee':remaning_fee,
            'paid_fee':paid_fee
        }
        return render(request, 'account/student_fee_detail.html', context)
    else:
        return redirect('school_mobile')
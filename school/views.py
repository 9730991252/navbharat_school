from navbharat_school.includes import * 
# Create your views here.
def save_clerk_used_count(c_id):
    obj, created = Clerk_used_count.objects.get_or_create(clerk_id=c_id, defaults={'used_count': 1})
    if not created:
        obj.used_count = F('used_count') + 1
        obj.save()

def school_home(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        messages.success(request, 'Welcome to NAVBHARAT ENGLISH MEDIUM SCHOOL KARMALA!')
        save_clerk_used_count(clerk.id)
        context={
            'clerk':clerk
        }
        return render(request, 'school_home.html', context)
    else:
        return redirect('school_login')
    
def school_expenses(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if 'add_cash_expenses'in request.POST:
            amount = request.POST.get('amount')
            remark = request.POST.get('remark')
            cdate = request.POST.get('date')
            Expenses(
                batch=clerk.batch,
                amount=amount,
                remark=remark,
                type='cash',
                added_by=clerk,
                date=cdate
            ).save()
            messages.success(request, 'Cash Expenses Added Successfully!')
            return redirect('school_expenses')
        if 'add_bank_expenses'in request.POST:
            amount = request.POST.get('amount')
            remark = request.POST.get('remark')
            from_bank = request.POST.get('from_bank')
            check_number = request.POST.get('check_number')
            bdate = request.POST.get('date')
            Expenses(
                batch=clerk.batch,
                amount=amount,
                remark=remark,
                type='bank',
                added_by=clerk,
                from_bank_id=from_bank,
                check_number=check_number,
                date=bdate
            ).save()
            messages.success(request, 'Bank Expenses Added Successfully!')
            return redirect('school_expenses')
        if 'edit_cash_expense' in request.POST:
            exp_id = request.POST.get('expense_id')
            expense = Expenses.objects.get(id=exp_id)
            expense.amount = request.POST.get('amount')
            expense.remark = request.POST.get('remark')
            expense.date = request.POST.get('date')
            expense.updated_by = clerk
            expense.updated_date = datetime.now()
            expense.save()
            messages.success(request, 'Cash Expense Updated Successfully!')
            return redirect('school_expenses')

        if 'edit_bank_expense' in request.POST:
            exp_id = request.POST.get('expense_id')
            expense = Expenses.objects.get(id=exp_id)
            expense.amount = request.POST.get('amount')
            expense.remark = request.POST.get('remark')
            expense.date = request.POST.get('date')
            expense.from_bank_id = request.POST.get('from_bank')
            expense.check_number = request.POST.get('check_number')
            expense.updated_by = clerk
            expense.updated_date = datetime.now()
            expense.save()
            messages.success(request, 'Bank Expense Updated Successfully!')
            return redirect('school_expenses')
        context={
            'clerk':clerk,
            'expenses':Expenses.objects.filter(batch=clerk.batch),
            'bank_accounts':Bank_Account.objects.filter(status=1),
            'today_date':date.today()
        }
        return render(request, 'account/school_expenses.html', context)
    else:
        return redirect('school_login')

def student_fees(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        context={
            'clerk':clerk
        }
        return render(request, 'account/student_fees.html', context)
    else:
        return redirect('school_login')
    
def school_cash_transfer(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        avalable_cash = check_avalable_cash(request, clerk.batch)
        if 'transfer_cash_to_bank' in request.POST:
            transfer_amount = request.POST.get('transfer_amount')
            transfer_date = request.POST.get('transfer_date')
            to_bank = request.POST.get('to_bank')

            # Validate inputs
            if not transfer_amount or not transfer_date or not to_bank:
                messages.error(request, 'All fields are required for cash transfer.')
            elif not transfer_amount.isdigit() or int(transfer_amount) <= 0:
                messages.error(request, 'Invalid transfer amount.')
            else:
                if int(transfer_amount) > int(avalable_cash):
                    messages.error(request, 'You don\'t have enough cash.')
                else:
                    Cash_Transfer_To_Bank.objects.create(
                        batch=clerk.batch,
                        from_clerk=clerk,
                        to_bank_id=to_bank,
                        amount=transfer_amount,
                        transfer_date=transfer_date,
                    )
                    messages.success(request, 'Cash Transferred Successfully.')
            return redirect('school_cash_transfer')
        if 'transfer_cash_to_admin' in request.POST:
            transfer_amount = request.POST.get('transfer_amount')
            transfer_date = request.POST.get('transfer_date')
            # Validate inputs
            if not transfer_amount.isdigit() or int(transfer_amount) <= 0:
                messages.error(request, 'Invalid transfer amount.')
            else:
                if int(transfer_amount) > int(avalable_cash):
                    messages.error(request, 'You don\'t have enough cash.')
                else:
                    Cash_Transfer_To_Admin.objects.create(
                        batch=clerk.batch,
                        from_clerk=clerk,
                        amount=transfer_amount,
                        transfer_date=transfer_date,
                    )
                    messages.success(request, 'Cash Transferred Successfully.')
            return redirect('school_cash_transfer')
        if 'transfer_cash_to_bank_edit' in request.POST:
            id = request.POST.get('id')
            transfer_amount = request.POST.get('transfer_amount')
            transfer_date = request.POST.get('transfer_date')
            to_bank = request.POST.get('to_bank')

            # Validate inputs
            if not transfer_amount or not transfer_date or not to_bank:
                messages.error(request, 'All fields are required for cash transfer.')
            else:
                if int(float(transfer_amount)) > int(avalable_cash):
                    messages.error(request, 'You don\'t have enough cash.')
                else:
                    Cash_Transfer_To_Bank.objects.filter(id=id).update(
                        amount=transfer_amount,
                        transfer_date=transfer_date,
                        to_bank=to_bank,
                    )
                    messages.success(request, 'Cash Transfer Updated Successfully.')

            return redirect('school_cash_transfer')
        if 'transfer_cash_to_admin_edit' in request.POST:
            id = request.POST.get('id')
            transfer_amount = request.POST.get('transfer_amount')
            transfer_date = request.POST.get('transfer_date')

            # Validate inputs
            if not transfer_amount or not transfer_date:
                messages.error(request, 'All fields are required for cash transfer.')
            else:
                if int(float(transfer_amount)) > int(avalable_cash):
                    messages.error(request, 'You don\'t have enough cash.')
                else:
                    Cash_Transfer_To_Admin.objects.filter(id=id).update(
                        amount=transfer_amount,
                        transfer_date=transfer_date,
                    )
                    messages.success(request, 'Cash Transfer Updated Successfully.')

            return redirect('school_cash_transfer')
        context={
            'clerk':clerk,
            'avalable_cash':avalable_cash, 
            'bank':Bank_Account.objects.filter(status=1),
            'today_date':date.today(),
            'cash_transfer_to_bank':Cash_Transfer_To_Bank.objects.filter(batch=clerk.batch),
            'cash_transfer_to_admin':Cash_Transfer_To_Admin.objects.filter(batch=clerk.batch),
        }
        return render(request, 'account/school_cash_transfer.html', context)
    else:
        return redirect('school_login')

@csrf_exempt  # Only for testing; remove in production
def student_fee_detail(request, id):
    if request.session.get('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        student = get_object_or_404(Student, id=id)
        student_img = Student_Image.objects.filter(student=student).first()
        class_info = Class_student.objects.filter(student=student, batch=clerk.batch).select_related('batch', 'school_class').first()
        total_fee = Student_Total_Fee.objects.filter(student=student, added_by__batch=clerk.batch).first()
        remaning_fee = total_fee.total_fee if total_fee else 0
        cash_fee = Student_received_Fee_Cash.objects.filter(student=student, added_by__batch=clerk.batch)
        bank_fee = Student_recived_Fee_Bank.objects.filter(student=student, added_by__batch=clerk.batch)
        paid_fee = int(cash_fee.aggregate(Sum('received_amount'))['received_amount__sum'] or 0) + int(bank_fee.aggregate(Sum('recived_amount'))['recived_amount__sum'] or 0)
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
        
        # Save cash fee logic
        if 'save_bank_fee' in request.POST:
            bank = request.POST.get('bank')
            received_amount = request.POST.get('received_amount')
            pdate = request.POST.get('date')
            utr_number = request.POST.get('utr_number')
            # Save cash fee to database (if model exists)
            Student_recived_Fee_Bank.objects.create(
                student=student,
                added_by=clerk,
                recived_amount=received_amount,
                paid_date=pdate,
                account_id=bank,
                utr_number=utr_number,
            )
            messages.success(request, 'Bank Fee Saved successfully')
            return redirect('student_fee_detail', id=id)

        context = {
            'clerk': clerk,
            'student': student,
            'student_img': student_img,
            'class_info': class_info,
            'total_fee': total_fee,
            'todayes_date':date.today(),
            'cash_fee':cash_fee,
            'bank_fee':bank_fee,
            'remaning_fee':remaning_fee,
            'paid_fee':paid_fee,
            'accounts':Bank_Account.objects.filter(status=1)
        }
        return render(request, 'account/student_fee_detail.html', context)
    else:
        return redirect('school_login')

    
def add_bank_account(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if 'Add_Bank_Account' in request.POST:
            bank_name = request.POST.get('bank_name')
            account_number = request.POST.get('account_number')
            
            Bank_Account(
                added_by=clerk,
                bank_name=bank_name,
                account_number=account_number
            ).save()
            messages.success(request, 'Bank Account Added Successfully!')
            return redirect('add_bank_account')
        if 'edit_bank_account' in request.POST:
            id = request.POST.get('id')
            bank_name = request.POST.get('bank_name')
            account_number = request.POST.get('account_number')
            Bank_Account.objects.filter(id=id).update(
                bank_name=bank_name,
                account_number=account_number
            )
            messages.success(request, 'Bank Account Updated Successfully!')
            return redirect('add_bank_account')
        if 'active'in request.POST:
            bank_id = request.POST.get('id')
            bank = Bank_Account.objects.get(id=bank_id)
            bank.status = 0
            bank.save()
            return redirect('add_bank_account')
        if 'deactive'in request.POST:
            bank_id = request.POST.get('id')
            bank = Bank_Account.objects.get(id=bank_id)
            bank.status = 1
            bank.save()
            return redirect('add_bank_account')
        context={
            'clerk': clerk,
            'bank_accounts': Bank_Account.objects.filter(added_by=clerk)
        }
        return render(request, 'account/add_bank_account.html', context)
    else:
        return redirect('school_login')
    
@csrf_exempt
def holidays(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        
        if 'add_holi_day'in request.POST:
            date = request.POST.get('date')
            reason = request.POST.get('reason')
            if Holidays.objects.filter(date=date, added_by__batch=clerk.batch).exists():
                messages.error(request, 'This holiday is already registered!')
            else:
                Holidays.objects.create(
                    added_by=clerk,
                    date=date,
                    reason=reason
                )
                messages.success(request, 'Holiday added successfully!')
            return redirect('holidays')
        if 'delete_holiday' in request.POST:
            holiday_id = request.POST.get('holiday_id')
            holiday = Holidays.objects.filter(id=holiday_id).first()
            if holiday:
                holiday.delete()
                messages.warning(request, 'Holiday deleted successfully!')
            else:
                messages.error(request, 'Holiday not found!')
            return redirect('holidays')
        context={
            'clerk':clerk,
            'holidays': Holidays.objects.filter(added_by__batch=clerk.batch).order_by('-id'),
        }
        return render(request, 'holidays.html', context)
    else:
        return redirect('school_login')


@csrf_exempt
def student_image(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if 'add_image' in request.POST:
            id = request.POST.get('id')
            img_data = request.POST.get('img')  # base64 string

            format, imgstr = img_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{id}.{ext}')
            
            if Student_Image.objects.filter(student_id=id).exists():
                s = Student_Image.objects.filter(student_id=id).first()
                # Delete old image file from storage
                if s.image:
                    old_image_path = s.image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
            else:
                Student_Image.objects.create(student_id=id, added_by=clerk)
                
            s = Student_Image.objects.filter(student_id=id).first()
            s.image.save(f'{s.student.name}.webp', data, save=True)

            messages.success(request, 'Image Added Successfully')
        context={
            'clerk':clerk
        }
        return render(request, 'student/student_image.html', context)
    else:
        return redirect('school_login')


#teacher
def add_teacher(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        return_name = ''
        return_mobile = ''
        gender = ''
        aadhar_number = ''
        qualification = ''
        return_pin = ''
        if 'Add_Teacher' in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            aadhar_number = request.POST.get('aadhar_number')
            qualification = request.POST.get('qualification')

            # Basic validations
            if name == '':
                messages.error(request, 'Please enter teacher name!')
            elif mobile == '':
                messages.error(request, 'Please enter teacher mobile number!')
            elif pin == '':
                messages.error(request, 'Please enter teacher secret pin!')
            elif gender == '':
                messages.error(request, 'Please select teacher gender!')
            elif aadhar_number == '':
                messages.error(request, 'Please enter Aadhar number!')
            elif qualification == '':
                messages.error(request, 'Please enter qualification!')
            elif Teacher.objects.filter(mobile=mobile, batch=clerk.batch).exists():
                messages.error(request, 'This mobile number is already registered!')
            elif Teacher.objects.filter(aadhar_number=aadhar_number, batch=clerk.batch).exists():
                messages.error(request, 'This Aadhar number is already registered!')
            else:
                Teacher.objects.create(
                    batch=clerk.batch,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    gender=gender,
                    aadhar_number=aadhar_number,
                    qualification=qualification
                )
                messages.success(request, 'Teacher added successfully!')
                return redirect('add_teacher')
            return_name = name
            return_mobile = mobile
            return_pin = pin
        if 'edit_teacher' in request.POST:
            teacher_id = request.POST.get('teacher_id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            aadhar_number = request.POST.get('aadhar_number')
            qualification = request.POST.get('qualification')

            if name == '':
                messages.error(request, 'Please enter teacher name!')
            elif mobile == '':
                messages.error(request, 'Please enter teacher mobile number!')
            elif pin == '':
                messages.error(request, 'Please enter teacher secret pin!')
            elif gender == '':
                messages.error(request, 'Please select teacher gender!')
            elif aadhar_number == '':
                messages.error(request, 'Please enter Aadhar number!')
            elif qualification == '':
                messages.error(request, 'Please enter qualification!')
            elif Teacher.objects.filter(mobile=mobile, batch=clerk.batch).exclude(id=teacher_id).exists():
                messages.error(request, 'This mobile number is already registered!')
            elif Teacher.objects.filter(aadhar_number=aadhar_number, batch=clerk.batch).exclude(id=teacher_id).exists():
                messages.error(request, 'This Aadhar number is already registered!')
            else:
                Teacher.objects.filter(id=teacher_id).update(
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    gender=gender,
                    aadhar_number=aadhar_number,
                    qualification=qualification
                )
                messages.success(request, 'Teacher updated successfully!')
            return redirect('add_teacher')
        if 'active'in request.POST:
            teacher_id = request.POST.get('id')
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.status = 0
            teacher.save()
            return redirect('add_teacher')
        if 'deactive'in request.POST:
            teacher_id = request.POST.get('id')
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.status = 1
            teacher.save()
            return redirect('add_teacher')
        if 'Change_branding_status' in request.POST:
            teacher_id = request.POST.get('id')
            teacher = Teacher.objects.get(id=teacher_id)
            if teacher.branding_status == 1:
                teacher.branding_status = 0
            else:
                teacher.branding_status = 1
            teacher.save()
            return redirect('add_teacher')
        context={
            'clerk':clerk,
            'teachers': Teacher.objects.filter(batch=clerk.batch).order_by('-id'),
            'return_name': return_name,
            'return_mobile': return_mobile,
            'return_pin': return_pin,
            'return_gender': gender,
            'return_aadhar_number': aadhar_number,
            'return_qualification': qualification,
        }
        return render(request, 'teacher/add_teacher.html', context)
    else:
        return redirect('school_login')
    
#student
@csrf_exempt
def add_student(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        
        return_name = ''
        return_mobile = ''
        return_aadhar_number = ''
        return_address = ''
        if 'Add_Student'in request.POST:
            name = request.POST.get('name').lower()
            mobile = request.POST.get('mobile')
            aadhar_number = request.POST.get('aadhar_number')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            date_of_birth = request.POST.get('date_of_birth')
            if name == '':
                messages.error(request, 'Please enter Student name!')
            elif address == '':
                messages.error(request, 'Please enter Student address!')
            elif mobile == '':
                messages.error(request, 'Please enter Parent mobile number!')
            elif date_of_birth == '':
                messages.error(request, 'Please enter date_of_birth number!')

            elif aadhar_number == '':
                messages.error(request, 'Please enter Student Aadhar_number number!')
                
            elif gender == '':
                messages.error(request, 'Please Select Student gender!')
                

            elif Student.objects.filter(aadhar_number=aadhar_number).exists():
                messages.error(request, 'This Student is already registered!')
            else:
                Student(
                    name=name,
                    address=address,
                    mobile=mobile,
                    aadhar_number=aadhar_number,
                    secret_pin=pin or str('0000'),
                    gender=gender,
                    added_by=clerk,
                    date_of_birth=date_of_birth
                ).save()
                messages.success(request, 'Student added successfully!')
                return redirect('add_student')
            return_name = name
            return_address = address
            return_mobile = mobile
            return_aadhar_number = aadhar_number
        if 'edit_student' in request.POST:
            student_id = request.POST.get('student_id')
            name = request.POST.get('name').lower()
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            aadhar_number = request.POST.get('aadhar_number')
            pin = request.POST.get('pin')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            if name == '':
                messages.error(request, 'Please enter Student name!')
            elif address == '':
                messages.error(request, 'Please enter Student address!')
            elif mobile == '':
                messages.error(request, 'Please enter Parent mobile number!')

            elif aadhar_number == '':
                messages.error(request, 'Please enter Student Aadhar_number number!')
                
            elif date_of_birth == '':
                messages.error(request, 'Please Select Student date_of_birth!')
                
            elif gender == '':
                messages.error(request, 'Please Select Student gender!')
                
            elif Student.objects.filter(aadhar_number=aadhar_number).exclude(id=student_id).exists():
                messages.error(request, 'This Student is already registered!')
            else:
                Student.objects.filter(id=student_id).update(
                    name=name,
                    address=address,
                    mobile=mobile,
                    aadhar_number=aadhar_number,
                    secret_pin=pin,
                    gender=gender,
                    date_of_birth=date_of_birth
                )
                messages.success(request, 'Student updated successfully!')
                return redirect('add_student')
        if 'active'in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.status = 0
            student.save()
            return redirect('add_student')
        if 'deactive'in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.status = 1
            student.save()
            return redirect('add_student')
        if 'test'in request.POST:
            name = request.POST.get('name')
            print(name)
        s = Student.objects.all().order_by('name')[:20]
        context={
            'clerk':clerk,
            'students': s,
            'return_name': return_name,
            'return_mobile': return_mobile,
            'return_aadhar_number': return_aadhar_number,
            'return_address': return_address,
        }
        return render(request, 'student/add_student.html', context)
    else:
        return redirect('school_login')
    
#Class
def add_class(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()

        if 'Add_Class'in request.POST:
            name = request.POST.get('name').upper()

            if name == '':
                messages.error(request, 'Please enter class name!')
                
            elif School_class.objects.filter(name=name, batch=clerk.batch).exists():
                messages.error(request, 'This Class number is already registered!')
            else:
                School_class(
                    added_by=clerk,
                    batch=clerk.batch,
                    name=name
                ).save()
                messages.success(request, 'Clss added successfully!')
                return redirect('add_class')
        if 'edit_class' in request.POST:
            class_id = request.POST.get('class_id')
            name = request.POST.get('name')
            if name == '':
                messages.error(request, 'Please enter class name!')
            elif School_class.objects.filter(name=name, batch=clerk.batch).exclude(id=class_id).exists():
                messages.error(request, 'This mobile number is already registered!')
            else:
                School_class.objects.filter(id=class_id).update(name=name)
                messages.success(request, 'Class updated successfully!')
                return redirect('add_class')
        if 'active'in request.POST:
            Class_id = request.POST.get('id')
            c = School_class.objects.get(id=Class_id)
            c.status = 0
            c.save()
            return redirect('add_class')
        if 'deactive'in request.POST:
            Class_id = request.POST.get('id')
            c = School_class.objects.get(id=Class_id)
            c.status = 1
            c.save()
            return redirect('add_class')
        context={
            'clerk':clerk,
            'classes': School_class.objects.filter(batch=clerk.batch).order_by('-id'),
        }

        return render(request, 'class/add_class.html', context)
    else:
        return redirect('school_login')
    
def select_student_class(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()

        context={
            'clerk':clerk,
            'classes': School_class.objects.filter(batch=clerk.batch).order_by('-id'),
        }

        return render(request, 'class/select_student_class.html', context)
    else:
        return redirect('school_login')
    
@csrf_exempt
def select_student_class_id(request, id):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        if 'remove_selected_student'in request.POST:
            tid = request.POST.get('id')
            c = Class_student.objects.filter(id=tid).first()
            messages.success(request, f'Removed Student {c.student.name}')
            c.delete()
            return redirect(f'/school/select_student_class/{id}/')
        context={
            'clerk':clerk,
            'selected_students':Class_student.objects.filter(school_class_id=id).order_by('id'),
            'class':School_class.objects.filter(id=id).first()
        }

        return render(request, 'class/select_student_class_id.html', context)
    else:
        return redirect('school_login')
    
@csrf_exempt
def select_class_teacher(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()
        classes = []
        selected_teacher_id = []
        for c in  School_class.objects.filter(added_by__batch=clerk.batch).order_by('-id'):
            cl = Class_teacher.objects.filter(school_class_id=c.id).first() or ''
            if cl:
                selected_teacher_id.append(cl.teacher_id)
            classes.append({
                'id':c.id,
                'name':c.name,
                'class_teacher':cl,
            })
        if 'select_class_teacher'in request.POST:
            class_id = request.POST.get('class_id')
            teacher_id = request.POST.get('teacher_id')
            cl = Class_teacher.objects.filter(school_class_id=class_id).first()
            if cl:
                cl.teacher_id = teacher_id
                cl.save
            else:
                Class_teacher(
                    added_by=clerk,
                    school_class_id=class_id,
                    teacher_id=teacher_id
                ).save()
            messages.success(request, 'Class teacher assigned successfully!')
            return redirect('select_class_teacher')
        if 'remove_class_teacher'in request.POST:
            id = request.POST.get('id')
            Class_teacher.objects.filter(school_class_id=id).delete()
            messages.success(request, 'Class teacher removed successfully!')
            return redirect('select_class_teacher')
        context={
            'clerk':clerk,
            'classes':classes,
            'teachers':Teacher.objects.filter(batch=clerk.batch).exclude(id__in=selected_teacher_id)
            
        }

        return render(request, 'class/select_class_teacher.html', context)
    else:
        return redirect('school_login')
    
def add_subject(request):
    if request.session.has_key('school_mobile'):
        mobile = request.session['school_mobile']
        clerk = Clerk.objects.filter(mobile=mobile).first()

        if 'Add_Subject' in request.POST:
            name = request.POST.get('name').upper()

            if name == '':
                messages.error(request, 'Please enter subject name!')
            elif Subject.objects.filter(name=name, added_by__batch=clerk.batch).exists():
                messages.error(request, 'This subject is already registered!')
            else:
                Subject(
                    added_by=clerk,
                    name=name
                ).save()
                messages.success(request, 'Subject added successfully!')
                return redirect('add_subject')
        if 'edit_subject' in request.POST:
            subject_id = request.POST.get('subject_id')
            name = request.POST.get('name').upper()
            if name == '':
                messages.error(request, 'Please enter subject name!')
            elif Subject.objects.filter(name=name, added_by__batch=clerk.batch).exclude(id=subject_id).exists():
                messages.error(request, 'This subject is already registered!')
            else:
                Subject.objects.filter(id=subject_id).update(name=name)
                messages.success(request, 'Subject updated successfully!')
                return redirect('add_subject')
        if 'active' in request.POST:
            subject_id = request.POST.get('id')
            subject = Subject.objects.get(id=subject_id)
            subject.status = 0
            subject.save()
            return redirect('add_subject')
        if 'deactive' in request.POST:
            subject_id = request.POST.get('id')
            subject = Subject.objects.get(id=subject_id)
            subject.status = 1
            subject.save()
            return redirect('add_subject')
        context = {
            'clerk': clerk,
            'subjects': Subject.objects.filter(added_by__batch=clerk.batch).order_by('-id'),
        }

        return render(request, 'subject/add_subject.html', context)
    else:
        return redirect('school_login')
    
@csrf_exempt
def select_subject_class_and_teacher(request):
    if not request.session.get('school_mobile'):
        return redirect('school_login')

    mobile = request.session['school_mobile']
    clerk = Clerk.objects.filter(mobile=mobile).first()

    if not clerk:
        messages.error(request, "Clerk not found.")
        return redirect('login')

    if 'select'in request.POST:
        subject_id = request.POST.get('subject_id')
        class_id = request.POST.get('class_id')
        teacher_id = request.POST.get('teacher_id')

        # Check for duplicates
        already_exists = Subject_class_and_teacher.objects.filter(
            subject_id=subject_id,
            school_class_id=class_id,
            teacher_id=teacher_id
        ).exists()

        if already_exists:
            messages.error(request, 'This subject-class-teacher combination is already selected.')
        else:
            Subject_class_and_teacher.objects.create(
                added_by=clerk,
                subject_id=subject_id,
                school_class_id=class_id,
                teacher_id=teacher_id
            )
            messages.success(request, 'Combination added successfully.')

        return redirect('select_subject_class_and_teacher')
    if 'remove'in request.POST:
        id = request.POST.get('id')
        Subject_class_and_teacher.objects.filter(id=id).delete()
        messages.success(request, 'Combination removed successfully.')
        return redirect('select_subject_class_and_teacher')
        
    # GET request
    batch = clerk.batch
    context = {
        'clerk': clerk,
        'classes': School_class.objects.filter(added_by__batch=batch).order_by('-id'),
        'subjects': Subject.objects.filter(added_by__batch=batch).order_by('-id'),
        'teachers': Teacher.objects.filter(batch=batch).order_by('-id'),
        'selected_subject_class_teacher': Subject_class_and_teacher.objects.filter(added_by__batch=batch)
    }

    return render(request, 'subject/select_subject_class_and_teacher.html', context)
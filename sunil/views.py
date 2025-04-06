from navbharat_school.includes import *
# Create your views here.
def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["first_number"])
        b =int(request.POST["seconde_number"])
        s = a+b
        su = sunil.objects.filter().first()
        if s == int(su.sum) :
            request.session['sunil_mobile'] = s
            return redirect('/sunil/sunil_home/')
        else:
            return redirect('sunil_login')
    return render(request, 'sunil_login.html')

def sunil_home(request):
    if request.session.has_key('sunil_mobile'):
        if 'Add_batch'in request.POST:
            name = request.POST.get('name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            Batch(
                name=name,
                start_date=start_date,
                end_date=end_date
            ).save()
            return redirect('sunil_home')
        if 'edit_batch' in request.POST:
            batch_id = request.POST.get('id')
            batch = Batch.objects.get(id=batch_id)
            batch.name = request.POST.get('name')
            batch.start_date = request.POST.get('start_date')
            batch.end_date = request.POST.get('end_date')
            batch.save()
            return redirect('sunil_home')
        if 'batch_active' in request.POST:
            batch_id = request.POST.get('id')
            batch = Batch.objects.get(id=batch_id)
            batch.status = 0
            batch.save()
            return redirect('sunil_home')
        if 'batch_deactive' in request.POST:
            batch_id = request.POST.get('id')
            batch = Batch.objects.get(id=batch_id)
            batch.status = 1
            batch.save()
            return redirect('sunil_home')
        
        if 'Add_clerk' in request.POST:
            batch_id = request.POST.get('batch_id')
            mobile = request.POST.get('mobile')
            
            if Clerk.objects.filter(batch_id=batch_id,mobile=mobile).exists():
                return redirect('sunil_home')
            else:
                Clerk(
                    batch_id=batch_id,
                    name=request.POST.get('name'),
                    mobile=mobile,
                    secret_pin=request.POST.get('secret_pin')
                ).save()
            return redirect('sunil_home')
        if 'edit_clerk' in request.POST:
            clerk_id = request.POST.get('id')
            mobile = request.POST.get('mobile')
            batch_id = request.POST.get('batch_id')
            
            if Clerk.objects.filter(mobile=mobile, batch_id=batch_id).exists():
                existing_clerk = Clerk.objects.get(mobile=mobile, batch_id=batch_id)
                if existing_clerk.id != int(clerk_id):
                    return redirect('sunil_home')
            clerk = Clerk.objects.get(id=clerk_id)
            clerk.name = request.POST.get('name')
            clerk.mobile = mobile
            clerk.secret_pin = request.POST.get('secret_pin')
            clerk.batch_id = batch_id
            clerk.save()
            return redirect('sunil_home')
        if 'clerk_active' in request.POST:
            clerk_id = request.POST.get('id')
            clerk = Clerk.objects.get(id=clerk_id)
            clerk.status = 0
            clerk.save()
            return redirect('sunil_home')
        if 'clerk_deactive' in request.POST:
            clerk_id = request.POST.get('id')
            clerk = Clerk.objects.get(id=clerk_id)
            clerk.status = 1
            clerk.save()
            return redirect('sunil_home')
        context = {
            'batches': Batch.objects.all().order_by('name'),
            'clerks': Clerk.objects.all().order_by('name'),
        }
        return render(request, 'sunil_home.html', context)
    else:
        return redirect('sunil_login')
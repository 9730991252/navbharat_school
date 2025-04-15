
from navbharat_school.includes import *

def search_student(request):
    if request.method == 'GET':
        words = request.GET['words']
        batch_id = request.GET['batch_id']
        student = []
        for s in Student.objects.filter(name__icontains=words):
            selected_status = 0
            c = Class_student.objects.filter(student=s, batch_id=batch_id).first()
            class_name = ''
            if c:
                class_name = c.school_class.name
                selected_status = 1
            print(class_name)
            student.append({
                'id':s.id,
                'name':s.name,
                'mobile':s.mobile,
                'aadhar_number':s.aadhar_number,
                'secret_pin':s.secret_pin,
                'gender':s.gender,
                'selected_status':selected_status,
                'selected_class':class_name
            })
        context = {
            'student':student[:10]
        }
        t = render_to_string('search_student.html', context)
    return JsonResponse({'t': t})
 
def search_student_image(request):
    if request.method == 'GET':
        words = request.GET['words']
        batch_id = request.GET['batch_id']
        student = []
        for s in Student.objects.filter(name__icontains=words):
            student.append({
                'id':s.id,
                'name':s.name,
                'mobile':s.mobile,
                'aadhar_number':s.aadhar_number,
                'secret_pin':s.secret_pin,
                'gender':s.gender,
                'img':Student_Image.objects.filter(student=s).first(),
            })
        context = {
            'student':student[:10]
        }
        t = render_to_string('search_student_image.html', context)
    return JsonResponse({'t': t})
 

def select_student(request):
    if request.method == 'GET':
        id = request.GET['id']
        batch_id = request.GET['batch_id']
        class_id = request.GET['class_id']
        clerk_id = request.GET['clerk_id']
        Class_student(
            added_by_id = clerk_id,
            batch_id = batch_id,
            school_class_id = class_id,
            student_id = id
        ).save()
        context = {
            'selected_students':Class_student.objects.filter(school_class_id=class_id).order_by('id')
        }
        t = render_to_string('select_student.html', context)
    return JsonResponse({'t': t})

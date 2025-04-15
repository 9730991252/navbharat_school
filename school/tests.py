from django.test import TestCase

# Create your tests here.
        if 'add_image'in request.POST:
            id = request.POST.get('id')
            img = request.FILES.get('img')
            compressed_image = compress_image(img)
            Student_Image.objects.create(
                student_id=id,
                added_by=clerk
            )
            s = Student_Image.objects.filter(student_id=id).first()
            s.image.save(f'{s.student.name}.webp', compressed_image, save=True)
            messages.success(request, 'Image Added Successfully')
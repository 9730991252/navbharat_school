from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def school_login(request):
    return render(request, 'home/school_login.html')

def admin_login(request):
    return render(request, 'home/admin_login.html')

def parent_login(request):
    return render(request, 'home/parent_login.html')

def teacher_login(request):
    return render(request, 'home/teacher_login.html')
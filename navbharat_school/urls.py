"""
URL configuration for navbharat_school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('sunil/', include('sunil.urls')),
    path('school/', include('school.urls')),
    path('student/', include('student.urls')),
    path('ajax/', include('ajax.urls')),
    path('teacher/', include('teacher.urls')),
    path('admin/', include('admin.urls')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

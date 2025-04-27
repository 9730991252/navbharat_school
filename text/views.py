import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Device
from firebase_admin import messaging
from django.shortcuts import render
from navbharat_school.includes import *

def index(request):
    return render(request, 'notifications.html')

def delete(request):
    Student_Attendance.objects.all().delete()
    return render(request, 'notifications.html')

@csrf_exempt
def save_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'status': 'error', 'message': 'No token provided'}, status=400)
            
            Device.objects.get_or_create(token=token)
            return JsonResponse({'status': 'success'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def send_push(request):
    try:
        device = Device.objects.first()
        if not device:
            return JsonResponse({'status': 'error', 'message': 'No devices registered'})
        
        message = messaging.Message(
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title='Hello from Django!',
                    body='This is a push notification',
                ),
            ),
            token='dm0k4a_4FalKCFUPN6SJSM:APA91bHW9mkNflvrDrVk_rzhBq6whgzhUlZ6JVnrzbWglCPQt1_RJomSvjs0izYtquaAZGzul0BzA26FZPW9bBdQyc18K9Xk1nIs0IdOksnIlKDotA1bq0U'
        )
        
        response = messaging.send(message)
        return JsonResponse({
            'status': 'success',
            'message_id': response
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
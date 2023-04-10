from django.http import HttpResponse, StreamingHttpResponse
import cv2
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as login, logout, authenticate
from django.contrib.auth.decorators import login_required
import numpy as np
from whiteowl.core.classes import FaceDetection

from whiteowl.core.models import Camera, Employee, Photo
from collections import defaultdict

face_auth_models = defaultdict(lambda: None)

curr_user = None

@login_required
def home(request):
    return render(request, "core/home.html")

def login_view(request):
    if request.user.is_authenticated: 
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
            
        context = {'form': form}
        return render(request, 'core/login.html', context)
    
    return render(request, "core/login.html")

def register(request):
    if request.user.is_authenticated: 
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("Boom Boom Boomer")
        if form.is_valid():
            form.save()
            return redirect('home')

        print(form.errors)
        context = {'form': form}
        return render(request, "core/register.html", context)

    return render(request, "core/register.html")
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def cameras_view(request):
    if  request.method == 'POST':
        
        if request.POST.get('action') == 'delete':
            camera_id = request.POST.get('camid')
            camera = Camera.objects.get(id=camera_id)
            camera.delete()
            return redirect('cameras')
        
        if request.POST.get('action') == 'edit':
            camera_url = request.POST.get('camurl')
            camera_id = request.POST.get('camid')
            camera_name = request.POST.get('camname')
            
            camera  = Camera.objects.get(id=camera_id)
            camera.url = camera_url
            camera.name = camera_name
            
            camera.save() 
           
            
        if request.POST.get('action') == 'create':  
            
            print("Boom Boom Boomer")
            camera_url = request.POST.get('camurl')
            camera_name = request.POST.get('camname')
            camera = Camera(user=request.user, url=camera_url, name=camera_name)
            camera.save()
            return redirect('cameras')
    
    user_cameras = Camera.objects.filter(user=request.user)
    context = {'cameras': user_cameras}
    return render(request, "core/cameras.html", context)

def employees_view(request):
    # collect all employees and their photos
    if  request.method == 'POST':
        if request.POST.get('action') == 'create':
            employee_name = request.POST.get('empname')
            employee_photo = request.FILES.get('empphoto')
            
            employee = Employee(user=request.user, name=employee_name)
            
            employee.save()
            
            photo = Photo(image=employee_photo, employee=employee)
            
            photo.save()
             
            return redirect('employees')

        if request.POST.get('action') == 'delete':
            employee_id = request.POST.get('empid')
            employee = Employee.objects.get(id=employee_id)
            employee.delete()
            return redirect('employees') 
    
    
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, "core/employees.html", context)


def employee_detail_view(request, pk):
    if request.method == 'POST':
        empphotos = request.FILES.getlist('empphotos')
        
        for photo in empphotos:
            employee = Employee.objects.get(id=pk)
            photo = Photo(image=photo, employee=employee)
            photo.save()
        
        
         
    
    
    employee = Employee.objects.get(id=pk)
    photos = Photo.objects.filter(employee=employee)
    
    context = {'employee': employee, 'photos': photos}
    return render(request, "core/employee-detail.html", context)


def employee_delphoto_view(request, pk, photo_id ):
    photo = Photo.objects.get(id=photo_id)
    photo.delete()
    return redirect('employee-detail', pk=photo.employee.id)

def dashboard (request):
    global curr_user
    curr_user = request.user
    
    if request.method == 'POST':
        camera_id = int(request.POST.get('camid'))
        camera = Camera.objects.get(id=camera_id)
        cameras = Camera.objects.filter(user=request.user)
        context = {'cameras': cameras, 'camera': camera}
        
        return render(request, "core/dashboard.html", context)
        

    cameras = Camera.objects.filter(user=request.user)
    context = {'cameras': cameras}
    return render(request, "core/dashboard.html",context)


import threading
from django.views.decorators import gzip


class VideoCamera(object):
    def __init__(self):
        url = "http://192.168.2.108:8080/video"
        self.video = cv2.VideoCapture(url)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        return image

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            
def gen(camera:VideoCamera, user):
    while True:
        frame = camera.get_frame()
        print(frame)
        print("Boom Boom Boomer")
        print(type(frame))
        
        face_auth = None
        
        if user.username in face_auth_models.keys():
            print ("FaceAuth for User exists") 
            face_auth = face_auth_models[user.username]
        else:
            print ("FaceAuth for User does not exist")
            face_auth = FaceDetection(user)
            face_auth_models[user.username] = face_auth 

        detected_frame = face_auth.recognize(frame)
        
        if  detected_frame is None:
            detected_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            detected_frame = cv2.imencode('.jpg', detected_frame)[1].tobytes()
        
        print("Detected frame : ", detected_frame)
        
        yield  (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + detected_frame + b'\r\n\r\n')
       
@gzip.gzip_page 
def video_feed(request):
    try:
        cam = VideoCamera()
        response = StreamingHttpResponse(gen(cam, curr_user), content_type="multipart/x-mixed-replace;boundary=frame")
        response['Content-Disposition'] = 'inline; filename=stream.mjpg'
        return response
    except:
        pass

    return "Boom Boom Boomer"
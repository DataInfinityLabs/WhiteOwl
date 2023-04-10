import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
import cv2

from django.contrib.auth.models import User
from .models import Photo, Employee

class FaceDetection:
    def findEncodings(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList 
    
    def __init__(self, user:User):
        self.employees = Employee.objects.filter(user=user)
        self.images = []
        self.classNames = []
        
        for employee in self.employees:
            self.classNames.append(employee.name)
            if employee.first_photo == None:
                continue
            image = cv2.imread(employee.first_photo[1:])
            print("KPS",image)
            self.images.append(image)
             
        self.encodeList = self.findEncodings(self.images)
        print("Encodings Complete")
        print(self.encodeList)
        
    def recognize(self, img):
        
        if img is None:
            return None
        
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeList, encodeFace)
            faceDis = face_recognition.face_distance(self.encodeList, encodeFace)
            matchIndex = np.argmin(faceDis)
            
            print("Match Index", matchIndex)
            
            if matches[matchIndex]:
                name = self.classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                return cv2.imencode('.jpg', img)[1].tobytes()

        # return a dummy image
        return cv2.imencode('.jpg', img)[1].tobytes()
    
user = User.objects.get(id=1)
face = FaceDetection(user)

print(face)
        
        
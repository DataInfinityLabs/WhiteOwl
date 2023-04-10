from django.db import models

from django.contrib.auth.models import User

class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Employee(models.Model):
    id  = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    @property
    def first_photo(self):
        try:
            return self.photos.first().image.url
        except AttributeError:
            return None

    
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='photos/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='photos')
    
    def __str__(self):
        return f'{self.image.name}'

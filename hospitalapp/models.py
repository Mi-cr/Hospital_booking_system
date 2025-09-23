from django.db import models

# Create your models here.
from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.models import User 
 
class CustomUser(AbstractUser): 
    user_type = models.CharField(default=1, max_length=200) 
    status = models.IntegerField(default=0) 
class Patient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True) 
    address=models.CharField(max_length=255,null=True)
    age=models.IntegerField(null=True)
    Gender = models.CharField(max_length=255) 
    contact=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to="image/",null=True,blank=True) 
    patient_id = models.CharField(max_length=50, unique=True, null=True, blank=False)
class depatment(models.Model):
    DepatmentName = models.CharField(max_length=255,null=True)
    Description = models.CharField(max_length=255,null=True)    
class doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    Department=models.ForeignKey(depatment,on_delete=models.CASCADE,null=True) 
    Address=models.CharField(max_length=255,null=True)
    Age=models.IntegerField(null=True)
    Contact=models.CharField(max_length=255,null=True)
    Image=models.ImageField(upload_to="simage/",null=True,blank=True) 
class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(depatment, on_delete=models.CASCADE,null=True)
    appointment_date = models.DateField(null=True)
    appointment_time = models.TimeField(null=True) 
    status = models.CharField(max_length=50, default="Pending",null=True)  # Pending, Approved, Disapproved
    op_number = models.CharField(max_length=20, null=True, blank=True)
    consulted = models.IntegerField(default=0)
    
    
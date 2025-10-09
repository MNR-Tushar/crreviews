from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from cr.models import *
from .manager import CustomUserManager
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):

    university=models.ForeignKey(University, on_delete=models.SET_NULL,related_name='user_profile',null=True,blank=True)
    department=models.ForeignKey(Department, on_delete=models.SET_NULL,related_name='user_profile',null=True,blank=True)
    profile_picture=models.ImageField(upload_to='profile_pictures/',null=True,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    student_id=models.CharField(max_length=50,unique=True)
    batch=models.CharField(max_length=20,null=True,blank=True)
    section=models.CharField(max_length=20,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    facebook_url=models.URLField(null=True,blank=True)
    instqgram_url=models.URLField(null=True,blank=True)
    linkedin_url=models.URLField(null=True,blank=True)
    role=models.CharField(max_length=20, default='student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #date_joined = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email
    
    def get_profile_picture(self):
        url=""
        try:
            url=self.profile_pictures.url
        except:
            url=""
        return url


    

    

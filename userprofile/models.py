from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from cr.models import *
from .manager import CustomUserManager
from django.utils.text import slugify
import os
# Create your models here.

def user_profile_picture_path(instance, filename):
    """User profile picture upload path"""
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.id}.{ext}"
    return os.path.join('users', f'user_{instance.id}', 'profile_pictures', filename)

class User(AbstractBaseUser,PermissionsMixin):

    university=models.ForeignKey(University, on_delete=models.SET_NULL,related_name='university',null=True,blank=True)
    department=models.ForeignKey(Department, on_delete=models.SET_NULL,related_name='department',null=True,blank=True)
    profile_picture=models.ImageField(upload_to=user_profile_picture_path,null=True,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    student_id=models.CharField(max_length=50,unique=True)
    batch=models.CharField(max_length=20,null=True,blank=True)
    section=models.CharField(max_length=20,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    facebook_url=models.URLField(null=True,blank=True)
    instagram_url=models.URLField(null=True,blank=True)
    linkedin_url=models.URLField(null=True,blank=True)
    role=models.CharField(max_length=20, default='student')
    slug=models.SlugField(blank=True,unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #date_joined = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name} {self.last_name}")
            slug = base_slug
            counter = 1
            # uniqueness check
            while User.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/media/users/default_profile.png'
    
    
        
    


    

    

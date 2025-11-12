from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from cr.models import *
from .manager import CustomUserManager
from django.utils.text import slugify
import os
import uuid
from django.utils import timezone as django_timezone
# Create your models here.

def user_profile_picture_path(instance, filename):
    """User profile picture upload path"""
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.id}.{ext}"
    return os.path.join('users', f'user_{instance.id}', 'profile_pictures', filename)

class User(AbstractBaseUser,PermissionsMixin):

    university=models.ForeignKey(University, on_delete=models.SET_NULL,related_name='university_user',null=True,blank=True)
    department=models.ForeignKey(Department, on_delete=models.SET_NULL,related_name='department_user',null=True,blank=True)
    profile_picture = models.CharField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10,default='M',blank=True,null=True)
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    student_id=models.CharField(max_length=50,unique=True,null=True,blank=True)
    batch=models.CharField(max_length=20,null=True,blank=True)
    dept_batch = models.CharField(max_length=20 , blank=True, null=True)
    section=models.CharField(max_length=20,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    facebook_url=models.URLField(default='https://www.facebook.com/')
    instagram_url=models.URLField(default='https://www.instagram.com/')
    linkedin_url=models.URLField(default='https://www.linkedin.com/')
    role=models.CharField(max_length=20, default='student')
    slug=models.SlugField(blank=True,unique=True)


    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(blank=True, null=True, editable=False)
    email_verification_token_created = models.DateTimeField(blank=True, null=True)


    password_reset_token = models.UUIDField(null=True, blank=True, editable=False)
    password_reset_token_created = models.DateTimeField(null=True, blank=True)




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
            if not self.email_verification_token:
                self.email_verification_token = uuid.uuid4()
                self.email_verification_token_created = django_timezone.now()
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_profile_picture_url(self):
        """Return profile picture URL or default"""
        if self.profile_picture:
            return self.profile_picture
        return '/static/images/default-avatar.png'
    
    def generate_password_reset_token(self):
        """Generate new password reset token"""
        self.password_reset_token = uuid.uuid4()
        self.password_reset_token_created = django_timezone.now()
        self.save()
        return self.password_reset_token
    
    def is_password_reset_token_valid(self):
        """Check if password reset token is still valid (1 hour)"""
        if not self.password_reset_token_created:
            return False
        time_diff = django_timezone.now() - self.password_reset_token_created
        return time_diff.total_seconds() < 3600  # 1 hour
    
    def is_email_verification_token_valid(self):
        """Check if email verification token is still valid (24 hours)"""
        if not self.email_verification_token_created:
            return False
        time_diff = django_timezone.now() - self.email_verification_token_created
        return time_diff.total_seconds() < 86400  # 24 hours
    
class SavedCR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_crs')
    cr_profile = models.ForeignKey(CrProfile, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cr_profile') 

    def __str__(self):
        return f"{self.user.get_full_name()} saved {self.cr_profile.name}"
    
    



    

    

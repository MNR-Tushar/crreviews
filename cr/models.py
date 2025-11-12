import uuid
from django.db import models
from django.utils.text import slugify
import os
from django.db.models import Avg
# Create your models here.

class University(models.Model):

    Public = "Public"
    Private = "Private"

    university_type = [
        (Public,"Public"),
        (Private,"Private"),
    ]


    title =models.CharField(max_length=100,unique=True,blank=False,null=False)
    type =models.CharField(max_length=100,choices=university_type)
    address=models.CharField(max_length=150, blank=True, null=True)
    slug=models.SlugField(blank=True,unique=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    daleted_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
class Department(models.Model):

    title=models.CharField(max_length=50,unique=True,blank=False,null=False)
    code=models.CharField(max_length=50,unique=True,blank=True,null=True)
    slug=models.SlugField(blank=True,unique=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    daleted_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)

def cr_profile_picture_path(instance, filename):
    """CR profile picture upload path"""
    ext = filename.split('.')[-1]
    filename = f"cr_profile_{instance.id}.{ext}"
    return os.path.join('cr_profiles', f'cr_{instance.id}', 'profile_pictures', filename)



class CrProfile(models.Model):
    user=models.OneToOneField('userprofile.User', on_delete=models.CASCADE,related_name='user_profile')
    university=models.ForeignKey(University, on_delete=models.CASCADE,related_name='university_crs')
    department=models.ForeignKey(Department, on_delete=models.CASCADE,related_name='department_crs')


    cr_status = models.CharField(
    max_length=20, 
    choices=[('Present', 'Present CR'), ('Former', 'Former CR')], 
    default='Present'
    )
    
    profile_picture = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10,default='M',blank=True,null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    st_id = models.CharField(max_length=50, unique=True)
    batch = models.CharField(max_length=20)
    dept_batch = models.CharField(max_length=20 , blank=True, null=True)
    section = models.CharField(max_length=10)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    facebook_url = models.URLField(default='https://www.facebook.com/')
    instagram_url = models.URLField(default='https://www.instagram.com/')
    linkedin_url = models.URLField(default='https://www.linkedin.com/')


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{uuid.uuid4().hex[:6]}")

        # if not self.id and self.profile_picture:
        #     saved_image = self.profile_picture
        #     self.profile_picture = None
        #     super().save(*args, **kwargs)
        #     self.profile_picture = saved_image

        super().save(*args, **kwargs)
    def get_profile_picture_url(self):
        """Return profile picture URL or default"""
        if self.profile_picture:
            return self.profile_picture
        return '/static/images/default-avatar.png'


    @property
    def average_rating(self):
        avg=self.cr_reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg,1) if avg else 0
 


class Review(models.Model):
    user = models.ForeignKey('userprofile.User', on_delete=models.CASCADE, related_name='userreviews')
    cr_profile = models.ForeignKey(CrProfile, on_delete=models.CASCADE, related_name='cr_reviews')

    rating = models.PositiveSmallIntegerField() 
    description = models.TextField(blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)
    anonymous_name = models.CharField(max_length=100, blank=True, null=True)
    
    #  Approval system for anonymous reviews
    is_approved = models.BooleanField(default=True)  # Auto-approve non-anonymous
    reviewed_by = models.ForeignKey(
        'userprofile.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_reviews',
        help_text="Admin who approved/rejected this review"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = [['user', 'cr_profile']]
        ordering = ['-created_at']

    def __str__(self):
        if self.is_anonymous:
            status = "Approved" if self.is_approved else "⏳ Pending"
            return f"Anonymous Review ({status}) on {self.cr_profile.name}"
        return f"Review by {self.user.get_full_name()} on {self.cr_profile.name}"

    def save(self, *args, **kwargs):

        if not self.is_anonymous and self.is_approved is None:
            self.is_approved = True
  
        if self.is_anonymous and self.is_approved is None:
            self.is_approved = False
        
        if not self.slug:
            base_slug = f"review-{self.cr_profile.id}-{uuid.uuid4().hex[:8]}"
            self.slug = slugify(base_slug)
        
        super().save(*args, **kwargs)
    
    def get_reviewer_name(self):
        if self.is_anonymous:
            return self.anonymous_name or "Anonymous User"
        return self.user.get_full_name() if self.user else "Anonymous User"
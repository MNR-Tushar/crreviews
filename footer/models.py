from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} {self.email} at {self.created_at}"
    
class Teck_Stack(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Teck Stack from {self.title} at {self.created_at}"

class Developer_Profile(models.Model):
    tack_stack = models.ManyToManyField(Teck_Stack, related_name='developer_profiles', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='developer_profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100)
    degisnation = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(max_length=1000, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    projects_built = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Developer Profile from {self.name} {self.email} at {self.created_at}"
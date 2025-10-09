from django.db import models
from django.utils.text import slugify
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
    slug=models.SlugField(null=True,blank=True,unique=True)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    dalete_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
class Department(models.Model):

    university=models.ForeignKey(University, on_delete=models.CASCADE,related_name='departments')
    title=models.CharField(max_length=50,unique=True,blank=False,null=False)
    code=models.CharField(max_length=50,unique=True,blank=True,null=True)
    slug=models.SlugField(null=True,blank=True,unique=True)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    dalete_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)

from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['email','first_name','last_name' ,'student_id']
    search_fields=['email','first_name','last_name','student_id','batch','section']
    list_filter=['email','first_name','last_name','student_id','batch','section']
    ordering=['first_name','last_name','batch']
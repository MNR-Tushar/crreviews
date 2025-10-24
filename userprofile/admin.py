from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['email','first_name','last_name' ,'student_id']
    search_fields=['email','first_name','last_name','student_id','batch','section']
    list_filter=['email','first_name','last_name','student_id','batch','section']
    ordering=['first_name','last_name','batch']

@admin.register(SavedCR)
class SavedCRAdmin(admin.ModelAdmin):
    list_display=['user','cr_profile']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'notice_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'notice_type', 'created_at']
    search_fields = ['title', 'message']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notice Information', {
            'fields': ('title', 'message', 'notice_type')
        }),
        ('Settings', {
            'fields': ('is_active', 'link')
        }),
    )
from django.contrib import admin
from .models import *
# Register your models here.
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

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
@admin.register(Teck_Stack)
class Teck_StackAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Developer_Profile)
class Developer_ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'user', 'device_type', 'browser', 'timestamp')
    list_filter = ('timestamp', 'device_type', 'browser')
    search_fields = ('ip_address', 'path', 'user__email')
    readonly_fields = ('ip_address', 'user_agent', 'path', 'method', 'user', 'country', 'city', 'device_type', 'browser', 'timestamp')
    ordering = ('-timestamp',)
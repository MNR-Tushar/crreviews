from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'address')
    search_fields = ('title', 'type', 'address')
    list_filter = ('type',)
    ordering = ('title',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'code',)
    search_fields = ('title', 'code')
    ordering = ('title',)

@admin.register(CrProfile)
class CrProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'st_id', 'user', 'university', 'department', 'batch', 'section')
    search_fields = ('name', 'st_id', 'user__email')
    list_filter = ('university', 'department', 'batch')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_reviewer_name', 'cr_profile', 'rating','is_approved','is_anonymous','created_at')
    search_fields = ('user__email', 'cr_profile__name')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
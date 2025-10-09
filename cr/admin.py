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
    list_display = ('university', 'title', 'code',)
    search_fields = ('university', 'title', 'code')
    list_filter = ('university',)
    ordering = ('university',)
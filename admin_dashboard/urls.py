from django.urls import path
from .views import *

urlpatterns = [
    path('admin_dashboard/',admin_dashboard,name="admin_dashboard"),

    # University URLs
    path('admin_dashboard/university/add/', add_university, name='add_university'),
    path('admin_dashboard/university/edit/<slug:slug>/', edit_university, name='edit_university'),
    path('admin_dashboard/university/delete/<slug:slug>/', delete_university, name='delete_university'),
    
    # Department URLs
    path('admin_dashboard/department/add/', add_department, name='add_department'),
    path('admin_dashboard/department/edit/<slug:slug>/', edit_department, name='edit_department'),
    path('admin_dashboard/department/delete/<slug:slug>/',delete_department, name='delete_department'),
    
]

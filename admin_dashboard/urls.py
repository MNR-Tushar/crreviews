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
    
    # CR URLs
    path('admin_dashboard/cr/add/', admin_add_cr, name='admin_add_cr'),
    path('admin_dashboard/cr/view/<slug:slug>/', admin_view_cr, name='admin_view_cr'),
    path('admin_dashboard/cr/edit/<slug:slug>/', admin_edit_cr, name='admin_edit_cr'),
    path('admin_dashboard/cr/delete/<slug:slug>/', admin_delete_cr, name='admin_delete_cr'),

    # Review URLs
    path('admin_dashboard/review/view/<slug:slug>/', admin_view_review, name='admin_view_review'),
    path('admin_dashboard/review/edit/<slug:slug>/', admin_edit_review, name='admin_edit_review'),
    path('admin_dashboard/review/delete/<slug:slug>/', admin_delete_review, name='admin_delete_review'),

    # User URLs
    path('admin_dashboard/user/view/<slug:slug>/', admin_view_user, name='admin_view_user'),
    path('admin_dashboard/user/edit/<slug:slug>/', admin_edit_user, name='admin_edit_user'),
    path('admin_dashboard/user/delete/<slug:slug>/', admin_delete_user, name='admin_delete_user'),


]

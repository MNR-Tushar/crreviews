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

    # Notice URLs
    path('admin_dashboard/notice/add/', add_notice, name='add_notice'),
    path('admin_dashboard/notice/view/<int:pk>/', view_notice, name='view_notice'),
    path('admin_dashboard/notice/edit/<int:pk>/', edit_notice, name='edit_notice'),
    path('admin_dashboard/notice/delete/<int:pk>/', delete_notice, name='delete_notice'),
    path('admin_dashboard/notice/toggle/<int:pk>/', toggle_notice, name='toggle_notice'),

    # Message URLs
    path('admin_dashboard/messages/', view_messages, name='view_messages'),
    path('admin_dashboard/message/read/<int:pk>/', mark_message_read, name='mark_message_read'),
    path('admin_dashboard/message/delete/<int:pk>/', delete_message, name='delete_message'),

    # Developer Profile URLs
    path('admin_dashboard/developer/add/', add_developer_profile, name='add_developer_profile'),
    path('admin_dashboard/developer/view/<int:pk>/', view_developer_profile, name='view_developer_profile'),
    path('admin_dashboard/developer/edit/<int:pk>/', edit_developer_profile, name='edit_developer_profile'),
    path('admin_dashboard/developer/delete/<int:pk>/', delete_developer_profile, name='delete_developer_profile'),
    
    # Tech Stack URLs
    path('admin_dashboard/tech-stack/add/', add_tech_stack, name='add_tech_stack'),
    path('admin_dashboard/tech-stack/edit/<int:pk>/', edit_tech_stack, name='edit_tech_stack'),
    path('admin_dashboard/tech-stack/delete/<int:pk>/', delete_tech_stack, name='delete_tech_stack'),
    
    path('admin_dashboard/analytics/visitors/', visitor_analytics, name='visitor_analytics'),
    path('admin_dashboard/analytics/block-ip/<str:ip_address>/', block_ip, name='block_ip'),



]

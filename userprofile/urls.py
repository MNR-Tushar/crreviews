from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login,name="login"),
    path('registration/',registration,name="registration"),
    path('logout/',logout,name="logout"),

    # Email Verification
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification_email, name='resend_verification'),
    path('verification-pending/', verification_pending, name='verification_pending'),
    
    # Password Reset
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uuid:token>/', reset_password, name='reset_password'),
    path('password-reset-done/', password_reset_done, name='password_reset_done'),

    path('user_dashboard/<str:slug>/',user_dasboard,name="user_dashboard"),
    path('view_profile/<str:slug>/',view_profile,name="view_profile"),
    path('user_view/<str:slug>/',user_view,name="user_view"),
    path('edit_user/<str:slug>/',edit_user,name="edit_user"),
    path('user_settings/',user_settings,name="settings"),

    path('save-cr/<str:slug>/', save_cr, name='save_cr'),
    path('remove-saved-cr/<str:slug>/', remove_saved_cr, name='remove_saved_cr'),

    path('change_password/', change_password, name='change_password'),
    

]

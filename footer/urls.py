from django.urls import path
from .views import *

urlpatterns = [
 
    path('about_us/', about_us, name='about_us'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-conditions/', terms_conditions, name='terms_conditions'),
    path('help-support/', help_support, name='help_support'),
    path('developer/', developer, name='developer'),
    path('contact-message/', contact_message, name='contact_message'),
]
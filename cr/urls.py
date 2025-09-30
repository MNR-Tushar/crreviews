from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('all_cr/',all_cr,name='all_cr'),
    path('latest_reviews/',latest_reviews,name='latest_reviews'),
    path('profile/',profile,name='profile'),
    path('newcr/',add_cr,name='add_cr'),
]

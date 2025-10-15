from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('all_cr/',all_cr,name='all_cr'),
    path('latest_reviews/',latest_reviews,name='latest_reviews'),
    path('cr_profile/<str:slug>/',cr_profile,name='cr_profile'),
    path('addcr/',add_cr,name='add_cr'),
    path('submit_review/<str:cr_slug>/',submit_review,name='submit_review'),
]
